from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import db
from app.schemas.kardex_schema import KardexDetalleResponse, KardexResponse
from app.services.kardex_service import listar_kardex

router = APIRouter(prefix="/kardex", tags=["Kardex"])

def get_db():
    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.get("/{id_producto}", response_model=List[KardexDetalleResponse])
def listar(id_producto: int,session: Session = Depends(get_db)):
    return listar_kardex(session,id_producto)