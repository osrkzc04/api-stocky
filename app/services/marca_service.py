from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.marca_model import Marca
from app.schemas.marca_schema import MarcaCreate,MarcaUpdate


def crear_marca(db: Session, data: MarcaCreate) -> Marca:
    marca = Marca(**data.model_dump())
    db.add(marca)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Marca ya existe (dni, teléfono o correo duplicado)."
        ) from e
    db.refresh(marca)
    return marca

def obtener_marca_por_id(db: Session, id_marca: int) -> Marca:
    marca = db.query(Marca).filter(Marca.id_marca == id_marca).first()
    if not marca:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marca no encontrado")
    return marca

def listar_marca(db: Session) -> list[Marca]:
    query = db.query(Marca)
    return query.order_by(Marca.nombre).all()

def actualizar_marca(db: Session, id_marca: int, data: MarcaUpdate) -> Marca:
    marca = obtener_marca_por_id(db, id_marca)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(marca, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo actualizar: dni, teléfono o correo duplicado."
        ) from e
    db.refresh(marca)
    return marca

def eliminar_marca(db: Session, id_marca: int) -> None:
    marca = obtener_marca_por_id(db, id_marca)
    db.delete(marca)
    db.commit()