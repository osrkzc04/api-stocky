from sqlalchemy.orm import Session
from fastapi import HTTPException

def crear_marca(db: Session, nombre: str):
    from app.models.marca_model import Marca  # Importar aquí para evitar dependencias circulares
    db_marca = Marca(nombre=nombre)
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

def obtener_todas_marcas(db: Session):
    from app.models.marca_model import Marca  # Importar aquí para evitar dependencias circulares
    return db.query(Marca).all()

def obtener_marca_por_id(db: Session, id_marca: int):
    from app.models.marca_model import Marca  # Importar aquí para evitar dependencias circulares
    marca = db.query(Marca).filter(Marca.id_marca == id_marca).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca

def actualizar_marca(db: Session, id_marca: int, nombre: str):
    marca = obtener_marca_por_id(db, id_marca)
    marca.nombre = nombre
    db.commit()
    db.refresh(marca)
    return marca

def eliminar_marca(db: Session, id_marca: int):
    marca = obtener_marca_por_id(db, id_marca)
    db.delete(marca)
    db.commit()
    return {"message": "Marca eliminada"}