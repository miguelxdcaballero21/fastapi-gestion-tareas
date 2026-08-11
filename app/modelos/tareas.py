from datetime import date
from pydantic import BaseModel

from app.modelos.usuarios import UsuarioRespuesta


class Tarea(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    avance: int
    fecha_inicio: date
    fecha_final: date
    usuario_id: int


class TareaActualizar(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    avance: int
    fecha_inicio: date
    fecha_final: date


class TareaRespuesta(Tarea):
    id: int


class TareaLista(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    avance: int
    fecha_inicio: date
    fecha_final: date

    usuario: UsuarioRespuesta
    actividades: list