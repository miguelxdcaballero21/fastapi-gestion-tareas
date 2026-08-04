from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

import os

load_dotenv()

URL_BASE_DATOS = os.getenv("DATABASE_URL")

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