from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.conexion_db import SesionDependencia
from app.modelos.tareas import (
    Tarea,
    TareaCrear,
    TareaActualizar,
    TareaRespuesta,
    TareaLista
)
from app.modelos.usuarios import Usuario

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"]
)


@router.post("/", response_model=TareaRespuesta)
def crear_tarea(
    tarea: TareaCrear,
    sesion: SesionDependencia
):

    usuario = sesion.get(
        Usuario,
        tarea.usuario_id
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    nueva_tarea = Tarea(
        nombre=tarea.nombre,
        descripcion=tarea.descripcion,
        estado=tarea.estado,
        avance=tarea.avance,
        fecha_inicio=tarea.fecha_inicio,
        fecha_final=tarea.fecha_final,
        usuario_id=tarea.usuario_id
    )

    sesion.add(nueva_tarea)
    sesion.commit()
    sesion.refresh(nueva_tarea)

    return nueva_tarea


@router.get("/", response_model=list[TareaLista])
def listar_tareas(
    sesion: SesionDependencia
):

    tareas = sesion.exec(
        select(Tarea)
    ).all()

    return tareas


@router.get("/{tarea_id}", response_model=TareaRespuesta)
def obtener_tarea(
    tarea_id: int,
    sesion: SesionDependencia
):

    tarea = sesion.get(
        Tarea,
        tarea_id
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="La tarea no existe"
        )

    return tarea


@router.put("/{tarea_id}", response_model=TareaRespuesta)
def actualizar_tarea(
    tarea_id: int,
    datos: TareaActualizar,
    sesion: SesionDependencia
):

    tarea = sesion.get(
        Tarea,
        tarea_id
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="La tarea no existe"
        )

    tarea.nombre = datos.nombre
    tarea.descripcion = datos.descripcion
    tarea.estado = datos.estado
    tarea.avance = datos.avance
    tarea.fecha_inicio = datos.fecha_inicio
    tarea.fecha_final = datos.fecha_final

    sesion.add(tarea)
    sesion.commit()
    sesion.refresh(tarea)

    return tarea


@router.delete("/{tarea_id}")
def eliminar_tarea(
    tarea_id: int,
    sesion: SesionDependencia
):

    tarea = sesion.get(
        Tarea,
        tarea_id
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="La tarea no existe"
        )

    sesion.delete(tarea)
    sesion.commit()

    return {
        "mensaje": "Tarea eliminada correctamente"
    }
