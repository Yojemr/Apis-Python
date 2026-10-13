from bson import ObjectId
from src.models.database import collection
from src.models.model import TraineeModel, TraineeUpdateModel

def helper_trainee() -> dict:
    return {
        "id": str(trainee["id"]),
        "document": str(trainee["document"]),
        "firstname": str(trainee["firstname"]),
        "lastname": str(trainee["lastname"]),
        "email": str(trainee["email"]),
        "age": str(trainee["age"]),
        "program": str(trainee["program"]),
        "record_number": str(trainee["record_number"]),
    }