from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import db
from app.schemas.usuario_schema import LoginRequest, TokenResponse
from app.services.usuario_service import autenticar_usuario
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, datos.correo, datos.contrasena)
    token = create_access_token({"sub": usuario.correo, "id": usuario.id_usuario, "rol": usuario.rol,"name": usuario.nombre})
    return {"access_token": token, "token_type": "bearer"}