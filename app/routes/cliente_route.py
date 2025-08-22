from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import db
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services.cliente_service import (
    crear_cliente, listar_clientees, obtener_cliente_por_id,
    actualizar_cliente, eliminar_cliente,buscar_clientes_secuencial
)

router = APIRouter(prefix="/cliente", tags=["Cliente"])

def get_db():
    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear(data: ClienteCreate, session: Session = Depends(get_db)):
    return crear_cliente(session, data)

@router.get("/", response_model=List[ClienteResponse])
def listar(session: Session = Depends(get_db)):
    return listar_clientees(session)

@router.get("/buscar-secuencial", response_model=List[ClienteResponse])
def buscar_clientes(q: str = Query(..., min_length=1, description="Texto a buscar (dni o nombre)"),session: Session = Depends(get_db),):
    resultados = buscar_clientes_secuencial(session, q)
    return resultados

@router.get("/{id_cliente}", response_model=ClienteResponse)
def obtener(id_cliente: int, session: Session = Depends(get_db)):
    return obtener_cliente_por_id(session, id_cliente)

@router.put("/{id_cliente}", response_model=ClienteResponse)
def actualizar(id_cliente: int, data: ClienteUpdate, session: Session = Depends(get_db)):
    return actualizar_cliente(session, id_cliente, data)

@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_cliente: int, session: Session = Depends(get_db)):
    eliminar_cliente(session, id_cliente)
    return None

