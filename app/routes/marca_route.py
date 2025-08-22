from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import db
from app.schemas.marca_schema import MarcaCreate, MarcaResponse, MarcaUpdate
from app.services.marca_service import (
    crear_marca, listar_marca, obtener_marca_por_id,
    actualizar_marca, eliminar_marca
)

router = APIRouter(prefix="/marca", tags=["Marca"])

def get_db():
    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.post("/", response_model=MarcaResponse, status_code=status.HTTP_201_CREATED)
def crear(data: MarcaCreate, session: Session = Depends(get_db)):
    return crear_marca(session, data)

@router.get("/", response_model=List[MarcaResponse])
def listar(session: Session = Depends(get_db)):
    return listar_marca(session)

@router.get("/{id_marca}", response_model=MarcaResponse)
def obtener(id_marca: int, session: Session = Depends(get_db)):
    return obtener_marca_por_id(session, id_marca)

@router.put("/{id_marca}", response_model=MarcaResponse)
def actualizar(id_marca: int, data: MarcaUpdate, session: Session = Depends(get_db)):
    return actualizar_marca(session, id_marca, data)

@router.delete("/{id_marca}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_marca: int, session: Session = Depends(get_db)):
    eliminar_marca(session, id_marca)
    return None