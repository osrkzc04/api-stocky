from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.cliente_model import Cliente
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate

def crear_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(
        dni=cliente.dni,
        nombre=cliente.nombre,
        telefono=cliente.telefono,
        direccion=cliente.direccion,
        correo_electronico=cliente.correo_electronico
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def obtener_cliente_por_id(db: Session, id_cliente: int):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

def obtener_todos_clientes(db: Session):
    return db.query(Cliente).all()

def actualizar_cliente(db: Session, id_cliente: int, cliente: ClienteUpdate):
    db_cliente = obtener_cliente_por_id(db, id_cliente)
    db_cliente.dni = cliente.dni
    db_cliente.nombre = cliente.nombre
    db_cliente.telefono = cliente.telefono
    db_cliente.direccion = cliente.direccion
    db_cliente.correo_electronico = cliente.correo
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def eliminar_cliente(db: Session, id_cliente: int):
    db_cliente = obtener_cliente_por_id(db, id_cliente)
    db.delete(db_cliente)
    db.commit()
    return {"detail": "Cliente eliminado exitosamente"} 