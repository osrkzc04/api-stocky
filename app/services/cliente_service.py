from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.cliente_model import Cliente
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate

def crear_cliente(db: Session, data: ClienteCreate) -> Cliente:
    cliente = Cliente(**data.model_dump())
    db.add(cliente)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cliente ya existe (dni, teléfono o correo duplicado)."
        ) from e
    db.refresh(cliente)
    return cliente

def obtener_cliente_por_id(db: Session, id_cliente: int) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente

def listar_clientees(db: Session) -> list[Cliente]:
    query = db.query(Cliente)
    return query.order_by(Cliente.id_cliente).all()

def actualizar_cliente(db: Session, id_cliente: int, data: ClienteUpdate) -> Cliente:
    cliente = obtener_cliente_por_id(db, id_cliente)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cliente, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo actualizar: dni, teléfono o correo duplicado."
        ) from e
    db.refresh(cliente)
    return cliente

def eliminar_cliente(db: Session, id_cliente: int) -> None:
    cliente = obtener_cliente_por_id(db, id_cliente)
    db.delete(cliente)
    db.commit()


def buscar_clientes_secuencial(session: Session, q: str) -> List[Cliente]:
    q_lower = q.strip().lower()
    resultados = []

    clientes = session.query(Cliente).all()

    for cliente in clientes:
        if (
            q_lower in (cliente.dni or "").lower()
            or q_lower in (cliente.nombre or "").lower()
        ):
            resultados.append(cliente)

    return resultados