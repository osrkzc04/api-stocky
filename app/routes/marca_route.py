from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import db
from app.schemas.marca_schema import MarcaResponse

router = APIRouter(prefix="/marca", tags=["Marca"])

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/", response_model=MarcaResponse)
def crear_marca(nombre: str, db: Session = Depends(get_db)):
    from app.services.marca_service import crear_marca
    return crear_marca(db, nombre)

@router.get("/", response_model=list[MarcaResponse])
def obtener_todas_marcas(db: Session = Depends(get_db)):
    from app.services.marca_service import obtener_todas_marcas
    return obtener_todas_marcas(db)

@router.get("/{id_marca}", response_model=MarcaResponse)
def obtener_marca(id_marca: int, db: Session = Depends(get_db)):
    from app.services.marca_service import obtener_marca_por_id
    return obtener_marca_por_id(db, id_marca)   

@router.put("/{id_marca}", response_model=MarcaResponse)
def actualizar_marca(id_marca: int, nombre: str, db: Session = Depends(get_db)):
    from app.services.marca_service import actualizar_marca
    return actualizar_marca(db, id_marca, nombre)

@router.delete("/{id_marca}")
def eliminar_marca(id_marca: int, db: Session = Depends(get_db)):
    from app.services.marca_service import eliminar_marca
    return eliminar_marca(db, id_marca)

