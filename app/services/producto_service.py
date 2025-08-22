from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.producto_model import Producto
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate

def crear_producto(db: Session, data: ProductoCreate) -> Producto:
    producto = Producto(**data.model_dump())
    db.add(producto)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo crear el producto (código duplicado u otra restricción)."
        ) from e
    db.refresh(producto)
    return obtener_producto_por_id(db, producto.id_producto)

def obtener_producto_por_id(db: Session, id_producto: int) -> Producto:
    producto = (
        db.query(Producto)
        .options(joinedload(Producto.marca))
        .filter(Producto.id_producto == id_producto)
        .first()
    )
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto

def listar_productos(db: Session) -> list[Producto]:
    query = db.query(Producto).options(joinedload(Producto.marca))
    return query.order_by(Producto.id_producto).all()

def actualizar_producto(db: Session, id_producto: int, data: ProductoUpdate) -> Producto:
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(producto, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo actualizar el producto (posibles claves únicas)."
        ) from e
    db.refresh(producto)
    return obtener_producto_por_id(db, id_producto)

def eliminar_producto(db: Session, id_producto: int) -> None:
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    db.delete(producto)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo eliminar el producto (referencias existentes)."
        ) from e


def buscar_productos_secuencial(session: Session, q: str) -> list[Producto]:
    q_lower = q.strip().lower()
    resultados = []
    productos = session.query(Producto).all()

    for producto in productos:
        if (
            q_lower in (producto.codigo or "").lower()
            or q_lower in (producto.nombre or "").lower()
        ):
            resultados.append(producto)

    return resultados