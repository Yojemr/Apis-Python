import os
import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

with (
    patch.dict(os.environ, {"MONGO_URI": "mongodb://127.0.0.1:27017"}),
    patch("dotenv.load_dotenv"),
    patch("pymongo.MongoClient"),
):
    from src.templates.templates import router


class TraineeRoutesTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()
        app.include_router(router)
        self.client = TestClient(app)

    def test_update_trainee(self):
        with patch(
            "src.templates.templates.update_trainee",
            return_value={"id": "abc", "firstname": "Lina"},
        ) as update:
            response = self.client.put("/trainee/abc", json={"firstname": "Lina"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["firstname"], "Lina")
        update.assert_called_once()

    def test_update_missing_trainee(self):
        with patch("src.templates.templates.update_trainee", return_value=None):
            response = self.client.put("/trainee/invalid", json={"firstname": "Lina"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Aprendiz no encontrado")

    def test_delete_trainee(self):
        with patch("src.templates.templates.delete_trainee", return_value=True):
            response = self.client.delete("/trainee/abc")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")

    def test_delete_missing_trainee(self):
        with patch("src.templates.templates.delete_trainee", return_value=False):
            response = self.client.delete("/trainee/invalid")
        self.assertEqual(response.status_code, 404)
