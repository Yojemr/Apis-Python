import unittest

from pydantic import ValidationError

from src.models.model import TraineeModel, TraineeUpdateModel


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.data = dict(
            document="123",
            firstname="Ana",
            lastname="Maya",
            email="ana@example.com",
            age=20,
            program="ADSO",
            record_number=703,
        )

    def test_valid_model(self):
        model = TraineeModel(**self.data)
        self.assertEqual(model.age, 20)
        self.assertEqual(model.firstname, "Ana")

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            TraineeModel(**(self.data | {"email": "invalido"}))

    def test_missing_document(self):
        self.data.pop("document")
        with self.assertRaises(ValidationError):
            TraineeModel(**self.data)

    def test_empty_update(self):
        self.assertEqual(TraineeUpdateModel().model_dump(exclude_unset=True), {})

    def test_partial_update(self):
        update = TraineeUpdateModel(firstname="Maria")
        self.assertEqual(update.model_dump(exclude_unset=True), {"firstname": "Maria"})
