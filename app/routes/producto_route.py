from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import db
from app.schemas.producto_schema import (
    ProductoCreate, ProductoUpdate, ProductoResponse
)
from app.services.producto_service import (
    crear_producto, obtener_producto_por_id, listar_productos,
    actualizar_producto, eliminar_producto,buscar_productos_secuencial
)

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear(data: ProductoCreate, session: Session = Depends(get_db)):
    return crear_producto(session, data)

@router.get("/", response_model=List[ProductoResponse])
def listar(session: Session = Depends(get_db)):
    return listar_productos(session)

@router.get("/buscar-secuencial", response_model=List[ProductoResponse])
def buscar_productos(q: str = Query(..., min_length=1, description="Texto a buscar (código o nombre)"), session: Session = Depends(get_db)):
    resultados = buscar_productos_secuencial(session, q)
    return resultados

@router.get("/{id_producto}", response_model=ProductoResponse)
def obtener(id_producto: int, session: Session = Depends(get_db)):
    return obtener_producto_por_id(session, id_producto)

@router.put("/{id_producto}", response_model=ProductoResponse)
def actualizar(id_producto: int, data: ProductoUpdate, session: Session = Depends(get_db)):
    return actualizar_producto(session, id_producto, data)

@router.delete("/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_producto: int, session: Session = Depends(get_db)):
    eliminar_producto(session, id_producto)
    return None


