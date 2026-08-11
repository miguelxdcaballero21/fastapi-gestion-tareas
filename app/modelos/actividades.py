from datetime import date

from pydantic import BaseModel


class Actividad(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool
    tarea_id: int


class ActividadActualizar(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool


class ActividadRespuesta(Actividad):
    id: int