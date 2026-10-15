from src.models.database import collection
from src.models.model import TraineeModel


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


def create_trainee(trainee: TraineeModel):
    trainee_dict = trainee.model_dump()
    result = collection.insert_one(trainee_dict)
    new_trainee = collection.find_one({"_id": result.inserted_id})
    return helper_trainee(new_trainee)
