from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import db
from app.dependencies.auth import verificar_token
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import crear_usuario, obtener_usuario_por_id, obtener_todos_usuarios

router = APIRouter(prefix="/usuario", tags=["Usuario"])

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/", response_model=UsuarioResponse)
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)

@router.get("/", response_model=list[UsuarioResponse])
def obtener_todos(db: Session = Depends(get_db)):
    return obtener_todos_usuarios(db)
  
@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return obtener_usuario_por_id(db, id_usuario)