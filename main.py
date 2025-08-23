from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.routes import auth_route, cliente_route, kardex_route, marca_route, usuario_route,dashboard_route,compra_route,producto_route,proveedor_router,venta_route

app = FastAPI(
    title="Sistema de Gestión de Bodega",
    version="1.0.0",
    docs_url="/docs",  # opcional, puedes cambiarlo a otra ruta
    redoc_url="/redoc",  # también puedes personalizar o quitarlo
)

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "http://192.168.137.129",
    "http://192.168.100.6:3000",
    "http://localhost:4173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # o ["*"] para permitir todos (solo en desarrollo)
    allow_credentials=True,
    allow_methods=["*"],              # permite todos los métodos: GET, POST, PUT...
    allow_headers=["*"],              # permite todos los headers
)
app.include_router(auth_route.router)
app.include_router(cliente_route.router)
app.include_router(compra_route.router)
app.include_router(dashboard_route.router)
app.include_router(kardex_route.router)
app.include_router(marca_route.router)
app.include_router(producto_route.router)
app.include_router(proveedor_router.router)
app.include_router(usuario_route.router)
app.include_router(venta_route.router)

@app.get("/")
def read_root():
    return {"message": "API Bodega con FastAPI"}