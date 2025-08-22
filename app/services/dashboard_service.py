from sqlalchemy.orm import Session
from sqlalchemy import text

def obtener_totales(db: Session):
    query = text("SELECT * FROM obtener_totales()")
    result = db.execute(query).fetchone()
    return {
        "total_clientes": result[0],
        "total_proveedores": result[1],
        "total_ventas": result[2],
        "total_compras": result[3],
    }

def obtener_ventas_mensuales(db: Session):
    query = text("SELECT * FROM ventas_por_mes_actual()")
    result = db.execute(query).fetchall()

    ventas = {mes: 0 for mes in range(1, 13)}
    for row in result:
        mes, total = row
        ventas[int(mes)] = total

    return ventas

def obtener_compras_mensuales(db: Session):
    query = text("SELECT * FROM compras_por_mes_actual()")
    result = db.execute(query).fetchall()

    compras = {mes: 0 for mes in range(1, 13)}
    for row in result:
        mes, total = row
        compras[int(mes)] = total

    return compras