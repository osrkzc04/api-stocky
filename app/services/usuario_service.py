from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.core.security import hash_password, verify_password

def crear_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contrasena=hash_password(usuario.contrasena),
        rol=usuario.rol
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuario_por_id(db: Session, id_usuario: int) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

def obtener_todos_usuarios(db: Session):
    return db.query(Usuario).all()

def actualizar_usuario(db: Session, id_usuario: int, usuario: UsuarioCreate):
    db_usuario = obtener_usuario_por_id(db, id_usuario)
    db_usuario.nombre = usuario.nombre
    db_usuario.correo = usuario.correo
    db_usuario.contrasena = hash_password(usuario.contrasena)
    db_usuario.rol = usuario.rol
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def autenticar_usuario(db: Session, correo: str, contrasena: str) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario or not verify_password(contrasena, usuario.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return usuario