from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import db
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse
from app.services.cliente_service import actualizar_cliente, crear_cliente, eliminar_cliente, obtener_cliente_por_id, obtener_todos_clientes

router = APIRouter(prefix="/cliente", tags=["Cliente"])

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/", response_model=ClienteResponse)
def crear(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crear_cliente(db, cliente)

@router.get("/", response_model=list[ClienteResponse])
def obtener_todos(db: Session = Depends(get_db)): 
    return obtener_todos_clientes(db)

@router.get("/{id_cliente}", response_model=ClienteResponse)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return obtener_cliente_por_id(db, id_cliente)

@router.put("/{id_cliente}", response_model=ClienteResponse)
def actualizar(id_cliente: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    return actualizar_cliente(db, id_cliente, cliente)

@router.delete("/{id_cliente}")
def eliminar(id_cliente: int, db: Session = Depends(get_db)):
    return eliminar_cliente(db, id_cliente) 