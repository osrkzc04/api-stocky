from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import db
from app.services.dashboard_service import obtener_compras_mensuales, obtener_totales, obtener_ventas_mensuales

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.get("/totales")
def obtener_totales_dashboard(db: Session = Depends(get_db)):
    return obtener_totales(db)

@router.get("/ventas-mensuales")
def ventas_mensuales(db: Session = Depends(get_db)):
    return obtener_ventas_mensuales(db)

@router.get("/compras-mensuales")
def compras_mensuales(db: Session = Depends(get_db)):   
    return obtener_compras_mensuales(db)