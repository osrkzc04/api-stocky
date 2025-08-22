from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import db
from app.schemas.compra_schema import (
    CompraCreate,
    CompraUpdate,
    CompraDetalleResponse,
)
from app.services.compra_service import (
    crear_compra,
    obtener_compra_por_id,
    obtener_compras,
    actualizar_compra,
    eliminar_compra,
    obtener_ultimas_compras
)

router = APIRouter(prefix="/compras", tags=["Compras"])

def get_db():
    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/",response_model=CompraDetalleResponse,status_code=status.HTTP_201_CREATED,summary="Crear compra con múltiples detalles")
def crear(data: CompraCreate, session: Session = Depends(get_db)):
    return crear_compra(session, data)


@router.get("/",response_model=List[CompraDetalleResponse],summary="Listar todas las compras con relaciones")
def listar(session: Session = Depends(get_db)):
    return obtener_compras(session)

@router.get("/ultimasCompras",response_model=List[CompraDetalleResponse],summary="Obtener las 10 compras más recientes")
def ultimasCompras(session: Session = Depends(get_db)):
    return obtener_ultimas_compras(session)

@router.get("/{id_compra}",response_model=CompraDetalleResponse,summary="Obtener una compra por ID (con relaciones)")
def obtener(id_compra: int, session: Session = Depends(get_db)):
    return obtener_compra_por_id(session, id_compra)

@router.put("/{id_compra}",response_model=CompraDetalleResponse,summary="Actualizar compra (cabecera) y devolver con relaciones")
def actualizar(id_compra: int, data: CompraUpdate, session: Session = Depends(get_db)):
    return actualizar_compra(session, id_compra, data)

@router.delete("/{id_compra}",status_code=status.HTTP_204_NO_CONTENT,summary="Eliminar compra",)
def eliminar(id_compra: int, session: Session = Depends(get_db)):
    eliminar_compra(session, id_compra)
    return None
