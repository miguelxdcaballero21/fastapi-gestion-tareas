from fastapi import FastAPI

from app.conexion_db import crear_bd

from app.enrutadores.usuarios import router as router_usuarios
from app.enrutadores.tareas import router as router_tareas
from app.enrutadores.actividades import router as router_actividades

crear_bd()

app = FastAPI(
    title="Gestión de Tareas",
    version="1.0.0"
)

app.include_router(router_usuarios)
app.include_router(router_tareas)
app.include_router(router_actividades)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API Gestión de Tareas"
    }