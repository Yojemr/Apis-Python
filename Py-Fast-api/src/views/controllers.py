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