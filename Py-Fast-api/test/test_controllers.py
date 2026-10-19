import os
import unittest
from unittest.mock import patch

from bson import ObjectId

from src.models.model import TraineeModel, TraineeUpdateModel

with (
    patch.dict(os.environ, {"MONGO_URI": "mongodb://127.0.0.1:27017"}),
    patch("dotenv.load_dotenv"),
    patch("pymongo.MongoClient"),
):
    from src.views.controllers import (
        create_trainee,
        delete_trainee,
        get_trainee_by_id,
        helper_trainee,
        update_trainee,
    )


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

    def test_invalid_object_ids_do_not_query_mongodb(self):
        with patch("src.views.controllers.collection") as collection:
            self.assertIsNone(get_trainee_by_id("incorrect"))
            self.assertIsNone(
                update_trainee("incorrect", TraineeUpdateModel(firstname="Lina"))
            )
            self.assertFalse(delete_trainee("incorrect"))

            collection.find_one.assert_not_called()
            collection.update_one.assert_not_called()
            collection.delete_one.assert_not_called()

    def test_partial_update_preserves_other_fields(self):
        oid = ObjectId()
        trainee = {
            "_id": oid,
            "document": "123",
            "firstname": "Lina",
            "lastname": "Maya",
            "email": "lina@example.com",
            "age": 20,
            "program": "ADSO",
            "record_number": 703,
        }
        with patch("src.views.controllers.collection") as collection:
            collection.find_one.return_value = trainee

            result = update_trainee(
                str(oid), TraineeUpdateModel(firstname="Lina")
            )

            collection.update_one.assert_called_once_with(
                {"_id": oid}, {"$set": {"firstname": "Lina"}}
            )
            self.assertEqual(result["id"], str(oid))

    def test_empty_update_does_not_write_to_mongodb(self):
        oid = ObjectId()
        trainee = {
            "_id": oid,
            "document": "123",
            "firstname": "Ana",
            "lastname": "Maya",
            "email": "ana@example.com",
            "age": 20,
            "program": "ADSO",
            "record_number": 703,
        }
        with patch("src.views.controllers.collection") as collection:
            collection.find_one.return_value = trainee

            result = update_trainee(str(oid), TraineeUpdateModel())

            self.assertEqual(result["firstname"], "Ana")
            collection.update_one.assert_not_called()

    def test_delete_existing_trainee(self):
        oid = ObjectId()
        with patch("src.views.controllers.collection") as collection:
            collection.find_one.return_value = {"_id": oid}

            self.assertTrue(delete_trainee(str(oid)))

            collection.delete_one.assert_called_once_with({"_id": oid})
