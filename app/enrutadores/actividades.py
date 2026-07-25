from fastapi import APIRouter, HTTPException

from app.listas import tareas, actividades
from app.modelos.actividades import Actividad,ActividadRespuesta,ActividadActualizar

router = APIRouter(
    tags=["Actividades"]
)


@router.post(
    "/tareas/{tarea_id}/actividades/",
    response_model=ActividadRespuesta
)
def crear_actividad(
    tarea_id: int,
    actividad: Actividad
):

    tarea = next(
        (t for t in tareas if t["id"] == tarea_id),
        None
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="La tarea no existe"
        )

    nueva_actividad = {
        "id": len(actividades) + 1,
        "nombre": actividad.nombre,
        "descripcion": actividad.descripcion,
        "estado": actividad.estado,
        "fecha": actividad.fecha,
        "completada": actividad.completada,
        "tarea_id": tarea_id
    }

    actividades.append(nueva_actividad)

    return nueva_actividad

@router.patch(
    "/actividades/{actividad_id}",
    response_model=ActividadRespuesta
)
def actualizar_actividad(
    actividad_id: int,
    datos: ActividadActualizar
):

    actividad = next(
        (a for a in actividades if a["id"] == actividad_id),
        None
    )

    if actividad is None:
        raise HTTPException(
            status_code=404,
            detail="La actividad no existe"
        )
    
    actividad["completada"] = datos.completada

    return actividad