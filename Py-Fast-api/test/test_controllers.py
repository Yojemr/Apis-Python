import unittest

from bson import ObjectId

from src.views.controllers import helper_trainee


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
