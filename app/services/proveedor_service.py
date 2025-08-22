from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.proveedor_model import Proveedor
from app.schemas.proveedor_schema import ProveedorCreate, ProveedorUpdate

def crear_proveedor(db: Session, data: ProveedorCreate) -> Proveedor:
    proveedor = Proveedor(**data.model_dump())
    db.add(proveedor)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Proveedor ya existe (dni, teléfono o correo duplicado)."
        ) from e
    db.refresh(proveedor)
    return proveedor

def obtener_proveedor_por_id(db: Session, id_proveedor: int) -> Proveedor:
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor

def listar_proveedores(db: Session) -> list[Proveedor]:
    query = db.query(Proveedor)
    return query.order_by(Proveedor.id_proveedor).all()

def actualizar_proveedor(db: Session, id_proveedor: int, data: ProveedorUpdate) -> Proveedor:
    proveedor = obtener_proveedor_por_id(db, id_proveedor)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(proveedor, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo actualizar: dni, teléfono o correo duplicado."
        ) from e
    db.refresh(proveedor)
    return proveedor

def eliminar_proveedor(db: Session, id_proveedor: int) -> None:
    proveedor = obtener_proveedor_por_id(db, id_proveedor)
    db.delete(proveedor)
    db.commit()


def buscar_proveedors_secuencial(session: Session, q: str) -> List[Proveedor]:
    q_lower = q.strip().lower()
    resultados = []
    proveedors = session.query(Proveedor).all()

    for proveedor in proveedors:
        if (
            q_lower in (proveedor.dni or "").lower()
            or q_lower in (proveedor.nombre or "").lower()
        ):
            resultados.append(proveedor)

    return resultados