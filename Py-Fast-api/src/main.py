from fastapi import FastAPI, HTTPException, status

from src.models.model import TraineeModel, TraineeUpdateModel
from src.templates.templates import router as trainee_router
from src.views.controllers import (
    create_trainee,
    delete_trainee,
    get_all_trainees,
    get_trainee_by_id,
    update_trainee,
)

app = FastAPI(
    title="Gestión de datos de los aprendices",
    description="API para gestionar los datos de los aprendices",
    version="1.0.0",
)

app.include_router(trainee_router)


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de gestión de datos de los aprendices"}


@app.post("/trainee", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_trainee_api(trainee: TraineeModel):
    # Se conserva la ruta singular para compatibilidad con las llamadas existentes.
    return create_trainee(trainee)


#obtener la lista de aprendices
@app.get("/trainees", response_description="Listar todos los aprendices")
def get_all_trainee_api():
    return get_all_trainees()


@app.get("/trainee/{id}", response_description="Obtener un aprendiz por su ID")
def get_trainee_by_id_api(id: str):
    trainee = get_trainee_by_id(id)
    if not trainee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aprendiz no encontrado"
        )
    return trainee


#actualizar datos de un aprendiz por su ID
@app.put("/trainee/{id}", response_description="Actualizar datos de un aprendiz por su ID")
def update_trainee_by_id_api(id: str, trainee: TraineeUpdateModel):
    trainee = update_trainee(id, trainee)
    if not trainee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aprendiz no encontrado"
        )
    return trainee


#Eliminar un aprendiz por su ID
@app.delete("/trainee/{id}", response_description="Eliminar un aprendiz por su ID")
def delete_trainee_by_id_api(id: str):
    trainee = delete_trainee(id)
    if not trainee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aprendiz no encontrado"
        )
    return {"message": "Aprendiz eliminado exitosamente"}
