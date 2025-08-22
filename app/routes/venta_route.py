from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import db
from app.schemas.venta_schema import (
    VentaCreate,
    VentaUpdate,
    VentaDetalleResponse,
)
from app.services.venta_service import (
    crear_venta,
    obtener_venta_por_id,
    obtener_ventas,
    actualizar_venta,
    eliminar_venta,
    obtener_ultimas_ventas
)

router = APIRouter(prefix="/ventas", tags=["Ventas"])

def get_db():
    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/",response_model=VentaDetalleResponse,status_code=status.HTTP_201_CREATED,summary="Crear venta con múltiples detalles")
def crear(data: VentaCreate, session: Session = Depends(get_db)):
    return crear_venta(session, data)


@router.get("/",response_model=List[VentaDetalleResponse],summary="Listar todas las ventas con relaciones")
def listar(session: Session = Depends(get_db)):
    return obtener_ventas(session)

@router.get("/ultimasVentas",response_model=List[VentaDetalleResponse],summary="Obtener las 10 ventas más recientes")
def ultimasVentas(session: Session = Depends(get_db)):
    return obtener_ultimas_ventas(session)

@router.get("/{id_venta}",response_model=VentaDetalleResponse,summary="Obtener una venta por ID (con relaciones)")
def obtener(id_venta: int, session: Session = Depends(get_db)):
    return obtener_venta_por_id(session, id_venta)

@router.put("/{id_venta}",response_model=VentaDetalleResponse,summary="Actualizar venta (cabecera) y devolver con relaciones")
def actualizar(id_venta: int, data: VentaUpdate, session: Session = Depends(get_db)):
    return actualizar_venta(session, id_venta, data)

@router.delete("/{id_venta}",status_code=status.HTTP_204_NO_CONTENT,summary="Eliminar venta",)
def eliminar(id_venta: int, session: Session = Depends(get_db)):
    eliminar_venta(session, id_venta)
    return None
