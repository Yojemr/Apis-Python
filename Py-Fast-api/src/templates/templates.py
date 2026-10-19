from fastapi import APIRouter, HTTPException, Response, status

from src.models.model import TraineeUpdateModel
from src.views.controllers import delete_trainee, update_trainee

router = APIRouter()


@router.put("/trainee/{id}", response_description="Actualizar un aprendiz por su ID")
def update_trainee_api(id: str, trainee: TraineeUpdateModel):
    updated = update_trainee(id, trainee)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aprendiz no encontrado"
        )
    return updated


@router.delete("/trainee/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trainee_api(id: str):
    if not delete_trainee(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aprendiz no encontrado"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
