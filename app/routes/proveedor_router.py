from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import db
from app.schemas.proveedor_schema import ProveedorCreate, ProveedorResponse, ProveedorUpdate
from app.services.proveedor_service import (
    crear_proveedor, listar_proveedores, obtener_proveedor_por_id,
    actualizar_proveedor, eliminar_proveedor,buscar_proveedors_secuencial
)

router = APIRouter(prefix="/proveedor", tags=["Proveedor"])

def get_db():
    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
def crear(data: ProveedorCreate, session: Session = Depends(get_db)):
    return crear_proveedor(session, data)

@router.get("/", response_model=List[ProveedorResponse])
def listar(session: Session = Depends(get_db)):
    return listar_proveedores(session)

@router.get("/buscar-secuencial", response_model=List[ProveedorResponse])
def buscar_proveedors(q: str = Query(..., min_length=1, description="Texto a buscar (dni o nombre)"),session: Session = Depends(get_db),):
    resultados = buscar_proveedors_secuencial(session, q)
    return resultados

@router.get("/{id_proveedor}", response_model=ProveedorResponse)
def obtener(id_proveedor: int, session: Session = Depends(get_db)):
    return obtener_proveedor_por_id(session, id_proveedor)

@router.put("/{id_proveedor}", response_model=ProveedorResponse)
def actualizar(id_proveedor: int, data: ProveedorUpdate, session: Session = Depends(get_db)):
    return actualizar_proveedor(session, id_proveedor, data)

@router.delete("/{id_proveedor}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_proveedor: int, session: Session = Depends(get_db)):
    eliminar_proveedor(session, id_proveedor)
    return None

