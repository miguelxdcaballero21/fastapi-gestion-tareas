from fastapi import APIRouter, HTTPException

from app.listas import usuarios, tareas, actividades
from app.modelos.tareas import Tarea, TareaRespuesta, TareaLista

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"]
)

@router.post("/", response_model=TareaRespuesta)
def crear_tarea(tarea: Tarea):

    # Validar que el usuario exista
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
