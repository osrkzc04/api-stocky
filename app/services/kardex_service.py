from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.kardex_model import Kardex
from app.schemas.kardex_schema import KardexCreate, KardexUpdate
from sqlalchemy.orm import joinedload

def listar_kardex(db: Session,id_producto:int) -> List[Kardex]:
    query = (
        db.query(Kardex)
         .options(joinedload(Kardex.producto), joinedload(Kardex.usuario))
         .filter(Kardex.id_producto == id_producto)
    )
    return query.order_by(Kardex.fecha.desc()).all()