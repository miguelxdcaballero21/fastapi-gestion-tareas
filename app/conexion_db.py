from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated

from fastapi import Depends

URL_BASE_DATOS = "sqlite:///gestion_tareas.db"

motor_bd = create_engine(
    URL_BASE_DATOS,
    echo=True
)


def crear_bd():
    SQLModel.metadata.create_all(motor_bd)


def obtener_sesion():
    with Session(motor_bd) as sesion:
        yield sesion


SesionDependencia = Annotated[
    Session,
    Depends(obtener_sesion)
]