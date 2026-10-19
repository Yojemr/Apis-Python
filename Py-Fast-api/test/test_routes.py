import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

with (
    patch.dict(os.environ, {"MONGO_URI": "mongodb://127.0.0.1:27017"}),
    patch("dotenv.load_dotenv"),
    patch("pymongo.MongoClient"),
):
    from src.main import app


class TraineeRoutesTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_crud_routes_are_registered_only_once(self):
        endpoints = (
            ("POST", "/trainee"),
            ("GET", "/trainees"),
            ("GET", "/trainee/{id}"),
            ("PUT", "/trainee/{id}"),
            ("DELETE", "/trainee/{id}"),
        )
        for method, path in endpoints:
            with self.subTest(method=method, path=path):
                matches = [
                    route
                    for route in app.routes
                    if getattr(route, "path", None) == path
                    and method in (getattr(route, "methods", None) or set())
                ]
                self.assertEqual(len(matches), 1)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Bienvenido", response.json()["message"])

    def test_create_trainee(self):
        payload = {
            "document": "123",
            "firstname": "Ana",
            "lastname": "Maya",
            "email": "ana@example.com",
            "age": 20,
            "program": "ADSO",
            "record_number": 703,
        }
        with patch(
            "src.main.create_trainee", return_value={"id": "abc", **payload}
        ) as create:
            response = self.client.post("/trainee", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], "abc")
        self.assertEqual(create.call_args.args[0].firstname, "Ana")

    def test_create_invalid_email(self):
        payload = {
            "document": "123",
            "firstname": "Ana",
            "lastname": "Maya",
            "email": "not-an-email",
            "age": 20,
            "program": "ADSO",
            "record_number": 703,
        }
        response = self.client.post("/trainee", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_list_trainees(self):
        data = [{"id": "abc", "firstname": "Ana"}]
        with patch("src.main.get_all_trainees", return_value=data):
            response = self.client.get("/trainees")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)

    def test_get_trainee(self):
        with patch(
            "src.main.get_trainee_by_id",
            return_value={"id": "abc", "firstname": "Ana"},
        ):
            response = self.client.get("/trainee/abc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["firstname"], "Ana")

    def test_get_missing_trainee(self):
        with patch("src.main.get_trainee_by_id", return_value=None):
            response = self.client.get("/trainee/invalid")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Aprendiz no encontrado")

    def test_update_trainee(self):
        with patch(
            "src.main.update_trainee",
            return_value={"id": "abc", "firstname": "Lina"},
        ) as update:
            response = self.client.put("/trainee/abc", json={"firstname": "Lina"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["firstname"], "Lina")
        self.assertEqual(update.call_args.args[1].firstname, "Lina")

    def test_update_missing_trainee(self):
        with patch("src.main.update_trainee", return_value=None):
            response = self.client.put("/trainee/invalid", json={"firstname": "Lina"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Aprendiz no encontrado")

    def test_delete_trainee(self):
        with patch("src.main.delete_trainee", return_value=True) as delete:
            response = self.client.delete("/trainee/abc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": "Aprendiz eliminado exitosamente"}
        )
        delete.assert_called_once_with("abc")

    def test_delete_missing_trainee(self):
        with patch("src.main.delete_trainee", return_value=False):
            response = self.client.delete("/trainee/invalid")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Aprendiz no encontrado")
