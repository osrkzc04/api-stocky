from decimal import Decimal
from typing import Iterable
from sqlalchemy import func
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

from app.models.compra_model import Compra
from app.models.detalle_compra_model import DetalleCompra
from app.models.producto_model import Producto
from app.schemas.compra_schema import (CompraCreate, CompraUpdate,DetalleCompraCreate)


def _eager_query(db: Session):
    return (
        db.query(Compra)
        .options(
            joinedload(Compra.proveedor),
            joinedload(Compra.usuario),
            selectinload(Compra.detalles).joinedload(DetalleCompra.producto),
        )
    )

def _calc_totales_desde_detalles(
    db: Session, detalles: Iterable[DetalleCompraCreate]
) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    subtotal = Decimal("0.0000")
    iva_15 = Decimal("0.0000")
    iva_0 = Decimal("0.0000")

    if not detalles:
        return subtotal, iva_15, iva_0, subtotal  

    ids = list({d.id_producto for d in detalles})
    productos = {p.id_producto: p for p in db.execute(
        select(Producto).where(Producto.id_producto.in_(ids))
    ).scalars().all()}

    for d in detalles:
        line_subtotal = Decimal(d.precio_unitario) * Decimal(d.cantidad)
        prod = productos.get(d.id_producto)
        if prod and getattr(prod, "iva", True):
            base = line_subtotal / Decimal("1.15")
            iva_line = line_subtotal - base
            subtotal += base
            iva_15 += iva_line
        else:
            subtotal += line_subtotal
            iva_0 += Decimal("0.0000")

    total = subtotal + iva_15
    return (subtotal.quantize(Decimal("0.0001")),
            iva_15.quantize(Decimal("0.0001")),
            iva_0.quantize(Decimal("0.0001")),
            total.quantize(Decimal("0.0001")))
    
def _next_numero_compra(db: Session) -> int:
    return db.query(func.coalesce(func.max(Compra.numero_compra), 0) + 1).scalar()

def crear_compra(db: Session, data: CompraCreate) -> Compra:
    print("Creando compra con datos:", data)
    if not getattr(data, "detalles", None):
        raise HTTPException(status_code=400, detail="La compra requiere al menos un detalle.")
    if any(getattr(data, f, None) is None for f in ("subtotal", "iva_15", "iva_0", "total")):
        sub, iva15, iva0, tot = _calc_totales_desde_detalles(db, data.detalles)
    else:
        sub, iva15, iva0, tot = data.subtotal, data.iva_15, data.iva_0, data.total

    num = _next_numero_compra(db)
    compra = Compra(
        numero_compra=num, 
        subtotal=sub,
        iva_15=iva15,
        iva_0=iva0,
        total=tot,
        id_proveedor=data.id_proveedor,
        id_usuario=data.id_usuario,
    )

    try:
        db.add(compra)
        db.flush() 

        for det in data.detalles:
            line_sub = det.subtotal if getattr(det, "subtotal", None) is not None \
                else Decimal(det.precio_unitario) * Decimal(det.cantidad)

            db.add(DetalleCompra(
                id_compra=compra.id_compra,
                id_producto=det.id_producto,
                cantidad=det.cantidad,
                precio_unitario=det.precio_unitario,
                subtotal=line_sub,
            ))

        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear la compra (verifique llaves foráneas y datos).",
        ) from e

    return obtener_compra_por_id(db, compra.id_compra)


def obtener_compra_por_id(db: Session, id_compra: int) -> Compra:
    compra = (
        _eager_query(db)
        .filter(Compra.id_compra == id_compra)
        .first()
    )
    if not compra:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra no encontrada")
    return compra


def obtener_compras(db: Session) -> list[Compra]:
    return (
        _eager_query(db)
        .order_by(Compra.id_compra)
        .all()
    )


def actualizar_compra(db: Session, id_compra: int, data: CompraUpdate) -> Compra:
    compra = db.query(Compra).filter(Compra.id_compra == id_compra).first()
    if not compra:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra no encontrada")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(compra, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar la compra.",
        ) from e

    return obtener_compra_por_id(db, id_compra)


def eliminar_compra(db: Session, id_compra: int) -> None:
    compra = db.query(Compra).filter(Compra.id_compra == id_compra).first()
    if not compra:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra no encontrada")

    try:
        db.delete(compra)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo eliminar la compra (posibles dependencias).",
        ) from e

def obtener_ultimas_compras(db: Session):
    return (
        db.query(Compra)
        .options(
            joinedload(Compra.proveedor),
            joinedload(Compra.usuario),
            selectinload(Compra.detalles).joinedload(DetalleCompra.producto),
        )
        .order_by(Compra.fecha.desc())
        .limit(10)
        .all()
    )