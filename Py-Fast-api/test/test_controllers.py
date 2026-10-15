import os
import unittest
from unittest.mock import patch

from bson import ObjectId

from src.models.model import TraineeModel

with (
    patch.dict(os.environ, {"MONGO_URI": "mongodb://127.0.0.1:27017"}),
    patch("dotenv.load_dotenv"),
    patch("pymongo.MongoClient"),
):
    from src.views.controllers import create_trainee, helper_trainee


class ControllerTests(unittest.TestCase):
    def test_serializes_mongodb_document(self):
        oid = ObjectId()
        data = dict(
            _id=oid,
            document="123",
            firstname="Ana",
            lastname="Maya",
            email="ana@example.com",
            age=20,
            program="ADSO",
            record_number=703,
        )
        result = helper_trainee(data)
        self.assertEqual(result["id"], str(oid))
        self.assertNotIn("_id", result)
        self.assertIsInstance(result["age"], int)
        self.assertIsInstance(result["record_number"], int)
        self.assertEqual(data["_id"], oid)

    def test_creates_and_serializes_trainee(self):
        trainee = TraineeModel(
            document="123",
            firstname="Ana",
            lastname="Maya",
            email="ana@example.com",
            age=20,
            program="ADSO",
            record_number=703,
        )
        oid = ObjectId()
        saved_document = {"_id": oid, **trainee.model_dump()}
        with patch("src.views.controllers.collection") as collection:
            collection.insert_one.return_value.inserted_id = oid
            collection.find_one.return_value = saved_document

            result = create_trainee(trainee)

            collection.insert_one.assert_called_once_with(trainee.model_dump())
            collection.find_one.assert_called_once_with({"_id": oid})

        self.assertEqual(result, {"id": str(oid), **trainee.model_dump()})
