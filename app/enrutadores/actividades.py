from fastapi import APIRouter, HTTPException

from app.conexion_db import SesionDependencia
from app.modelos.actividades import Actividad,ActividadCrear,ActividadActualizar,ActividadRespuesta
from app.modelos.tareas import Tarea
from sqlmodel import select

router = APIRouter(
    tags=["Actividades"]
)


@router.post(
    "/tareas/{tarea_id}/actividades/",
    response_model=ActividadRespuesta
)
def crear_actividad(
    tarea_id: int,
    actividad: ActividadCrear,
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

    nueva_actividad = Actividad(
        nombre=actividad.nombre,
        descripcion=actividad.descripcion,
        estado=actividad.estado,
        fecha=actividad.fecha,
        completada=actividad.completada,
        tarea_id=tarea_id
    )

    sesion.add(nueva_actividad)
    sesion.commit()
    sesion.refresh(nueva_actividad)

    return nueva_actividad


@router.get(
    "/actividades/",
    response_model=list[ActividadRespuesta]
)
def listar_actividades(
    sesion: SesionDependencia
):

    actividades = sesion.exec(
        select(Actividad)
    ).all()

    return actividades


@router.get(
    "/actividades/{actividad_id}",
    response_model=ActividadRespuesta
)
def obtener_actividad(
    actividad_id: int,
    sesion: SesionDependencia
):

    actividad = sesion.get(
        Actividad,
        actividad_id
    )

    if actividad is None:
        raise HTTPException(
            status_code=404,
            detail="La actividad no existe"
        )

    return actividad


@router.patch(
    "/actividades/{actividad_id}",
    response_model=ActividadRespuesta
)
def actualizar_actividad(
    actividad_id: int,
    datos: ActividadActualizar,
    sesion: SesionDependencia
):

    actividad = sesion.get(
        Actividad,
        actividad_id
    )

    if actividad is None:
        raise HTTPException(
            status_code=404,
            detail="La actividad no existe"
        )

    actividad.completada = datos.completada

    sesion.add(actividad)
    sesion.commit()
    sesion.refresh(actividad)

    return actividad


@router.delete("/actividades/{actividad_id}")
def eliminar_actividad(
    actividad_id: int,
    sesion: SesionDependencia
):

    actividad = sesion.get(
        Actividad,
        actividad_id
    )

    if actividad is None:
        raise HTTPException(
            status_code=404,
            detail="La actividad no existe"
        )

    sesion.delete(actividad)
    sesion.commit()

    return {
        "mensaje": "Actividad eliminada correctamente"
    }