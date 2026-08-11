from fastapi import APIRouter, HTTPException

from app.listas import usuarios, tareas, actividades
from app.modelos.tareas import (
    Tarea,
    TareaRespuesta,
    TareaLista,
    TareaActualizar
)

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"]
)


@router.post("/", response_model=TareaRespuesta)
def crear_tarea(tarea: Tarea):

    usuario = next(
        (u for u in usuarios if u["id"] == tarea.usuario_id),
        None
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    nueva_tarea = {
        "id": len(tareas) + 1,
        "nombre": tarea.nombre,
        "descripcion": tarea.descripcion,
        "estado": tarea.estado,
        "avance": tarea.avance,
        "fecha_inicio": tarea.fecha_inicio,
        "fecha_final": tarea.fecha_final,
        "usuario_id": tarea.usuario_id
    }

    tareas.append(nueva_tarea)

    return nueva_tarea


@router.get("/", response_model=list[TareaLista])
def listar_tareas():

    respuesta = []

    for tarea in tareas:

        usuario = next(
            (u for u in usuarios if u["id"] == tarea["usuario_id"]),
            None
        )

        actividades_tarea = [
            actividad
            for actividad in actividades
            if actividad["tarea_id"] == tarea["id"]
        ]

        respuesta.append(
            {
                "id": tarea["id"],
                "nombre": tarea["nombre"],
                "descripcion": tarea["descripcion"],
                "estado": tarea["estado"],
                "avance": tarea["avance"],
                "fecha_inicio": tarea["fecha_inicio"],
                "fecha_final": tarea["fecha_final"],
                "usuario": usuario,
                "actividades": actividades_tarea
            }
        )

    return respuesta


@router.get("/{tarea_id}", response_model=TareaRespuesta)
def obtener_tarea(tarea_id: int):

    tarea = next(
        (t for t in tareas if t["id"] == tarea_id),
        None
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="La tarea no existe"
        )

    return tarea


@router.patch("/{tarea_id}", response_model=TareaRespuesta)
def actualizar_tarea(
    tarea_id: int,
    datos: TareaActualizar
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

    tarea["nombre"] = datos.nombre
    tarea["descripcion"] = datos.descripcion
    tarea["estado"] = datos.estado
    tarea["avance"] = datos.avance
    tarea["fecha_inicio"] = datos.fecha_inicio
    tarea["fecha_final"] = datos.fecha_final

    return tarea


@router.delete("/{tarea_id}")
def eliminar_tarea(tarea_id: int):

    tarea = next(
        (t for t in tareas if t["id"] == tarea_id),
        None
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="La tarea no existe"
        )

    actividad_asociada = next(
        (
            a for a in actividades
            if a["tarea_id"] == tarea_id
        ),
        None
    )

    if actividad_asociada:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la tarea porque tiene actividades asociadas"
        )

    tareas.remove(tarea)

    return {
        "mensaje": "Tarea eliminada correctamente"
    }