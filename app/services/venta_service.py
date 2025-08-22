from decimal import Decimal
from typing import Iterable
from sqlalchemy import func
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

from app.models.venta_model import Venta
from app.models.detalle_venta_model import DetalleVenta
from app.models.producto_model import Producto
from app.schemas.venta_schema import (VentaCreate, VentaUpdate,DetalleVentaCreate)


def _eager_query(db: Session):
    return (
        db.query(Venta)
        .options(
            joinedload(Venta.cliente),
            joinedload(Venta.usuario),
            selectinload(Venta.detalles).joinedload(DetalleVenta.producto),
        )
    )

def _calc_totales_desde_detalles(
    db: Session, detalles: Iterable[DetalleVentaCreate]
) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    subtotal = Decimal("0.0000")
    iva_15 = Decimal("0.0000")
    iva_0 = Decimal("0.0000")

    if not detalles:
        return subtotal, iva_15, iva_0, subtotal  # total = 0

    # Traer IVA de los productos en un solo query
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
    
def _next_numero_venta(db: Session) -> int:
    return db.query(func.coalesce(func.max(Venta.numero_venta), 0) + 1).scalar()

def crear_venta(db: Session, data: VentaCreate) -> Venta:
    print("Creando venta con datos:", data)
    if not getattr(data, "detalles", None):
        raise HTTPException(status_code=400, detail="La venta requiere al menos un detalle.")
    if any(getattr(data, f, None) is None for f in ("subtotal", "iva_15", "iva_0", "total")):
        sub, iva15, iva0, tot = _calc_totales_desde_detalles(db, data.detalles)
    else:
        sub, iva15, iva0, tot = data.subtotal, data.iva_15, data.iva_0, data.total

    num = _next_numero_venta(db)
    venta = Venta(
        numero_venta=num, 
        subtotal=sub,
        iva_15=iva15,
        iva_0=iva0,
        total=tot,
        id_cliente=data.id_cliente,
        id_usuario=data.id_usuario,
    )

    try:
        db.add(venta)
        db.flush() 

        for det in data.detalles:
            line_sub = det.subtotal if getattr(det, "subtotal", None) is not None \
                else Decimal(det.precio_unitario) * Decimal(det.cantidad)

            db.add(DetalleVenta(
                id_venta=venta.id_venta,
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
            detail="No se pudo crear la venta (verifique llaves foráneas y datos).",
        ) from e

    return obtener_venta_por_id(db, venta.id_venta)


def obtener_venta_por_id(db: Session, id_venta: int) -> Venta:
    venta = (
        _eager_query(db)
        .filter(Venta.id_venta == id_venta)
        .first()
    )
    if not venta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")
    return venta


def obtener_ventas(db: Session) -> list[Venta]:
    return (
        _eager_query(db)
        .order_by(Venta.id_venta)
        .all()
    )


def actualizar_venta(db: Session, id_venta: int, data: VentaUpdate) -> Venta:
    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(venta, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar la venta.",
        ) from e

    return obtener_venta_por_id(db, id_venta)


def eliminar_venta(db: Session, id_venta: int) -> None:
    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

    try:
        db.delete(venta)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo eliminar la venta (posibles dependencias).",
        ) from e

def obtener_ultimas_ventas(db: Session):
    return (
        db.query(Venta)
        .options(
            joinedload(Venta.cliente),
            joinedload(Venta.usuario),
            selectinload(Venta.detalles).joinedload(DetalleVenta.producto),
        )
        .order_by(Venta.fecha.desc())
        .limit(10)
        .all()
    )