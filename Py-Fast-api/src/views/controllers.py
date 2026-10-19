from bson import ObjectId

from src.models.database import collection
from src.models.model import TraineeModel, TraineeUpdateModel


def helper_trainee(trainee: dict) -> dict:
    return {
        "id": str(trainee["_id"]),
        "document": str(trainee["document"]),
        "firstname": str(trainee["firstname"]),
        "lastname": str(trainee["lastname"]),
        "email": str(trainee["email"]),
        "age": trainee["age"],
        "program": str(trainee["program"]),
        "record_number": trainee["record_number"],
    }


# Crear datos de un aprendiz
def create_trainee(trainee: TraineeModel):
    trainee_dict = trainee.model_dump()
    result = collection.insert_one(trainee_dict)
    new_trainee = collection.find_one({"_id": result.inserted_id})
    return helper_trainee(new_trainee)


# Obtener todos los aprendices
def get_all_trainees():
    trainees = []
    for trainee in collection.find():
        trainees.append(helper_trainee(trainee))
    return trainees


# Obtener un aprendiz por su ID
def get_trainee_by_id(id: str):
    if not ObjectId.is_valid(id):
        return None
    trainee = collection.find_one({"_id": ObjectId(id)})
    if trainee:
        return helper_trainee(trainee)
    return None


# Actualizar datos del aprendiz
def update_trainee(id: str, data: TraineeUpdateModel):
    if not ObjectId.is_valid(id):
        return None
    trainee_id = ObjectId(id)
    data_update = data.model_dump(exclude_unset=True, exclude_none=True)
    if data_update:
        collection.update_one({"_id": trainee_id}, {"$set": data_update})
    trainee_updated = collection.find_one({"_id": trainee_id})
    if trainee_updated:
        return helper_trainee(trainee_updated)
    return None


# Eliminar datos del aprendiz por su ID
def delete_trainee(id: str):
    if not ObjectId.is_valid(id):
        return False
    trainee_id = ObjectId(id)
    trainee = collection.find_one({"_id": trainee_id})
    if trainee:
        collection.delete_one({"_id": trainee_id})
        return True
    return False
