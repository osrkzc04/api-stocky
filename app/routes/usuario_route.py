from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import db
from app.dependencies.auth import verificar_token
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import actualizar_usuario, crear_usuario, eliminar_usuario, listar_usuarios, obtener_usuario_por_id

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
def listar(db: Session = Depends(get_db)):
    return listar_usuarios(db)
  
@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return obtener_usuario_por_id(db, id_usuario)

@router.put("/{id_usuario}", response_model=UsuarioResponse, dependencies=[Depends(verificar_token)])
def actualizar(id_usuario: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return actualizar_usuario(db, id_usuario, usuario)

@router.delete("/{id_usuario}", dependencies=[Depends(verificar_token)])
def eliminar(id_usuario: int, db: Session = Depends(get_db)):
    eliminar_usuario(db, id_usuario) 
    return None
