import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "src/models/database.py"


def load_database():
    spec = importlib.util.spec_from_file_location("database_under_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DatabaseTests(unittest.TestCase):
    def test_import_keeps_client_open_without_connecting(self):
        with (
            patch.dict(os.environ, {"MONGO_URI": "mongodb://127.0.0.1:27017"}),
            patch("dotenv.load_dotenv") as dotenv,
            patch("pymongo.MongoClient") as mongo,
        ):
            module = load_database()
            dotenv.assert_called_once_with(MODULE_PATH.parents[2] / ".env")
            mongo.assert_called_once_with(
                "mongodb://127.0.0.1:27017",
                serverSelectionTimeoutMS=3000,
                connect=False,
            )
            self.assertIs(
                module.collection, mongo.return_value.database_apprentice.trainee
            )
            mongo.return_value.close.assert_not_called()
            mongo.return_value.admin.command.assert_not_called()

    def test_missing_uri_does_not_construct_client(self):
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("dotenv.load_dotenv"),
            patch("pymongo.MongoClient") as mongo,
        ):
            with self.assertRaisesRegex(RuntimeError, "MONGO_URI"):
                load_database()
            mongo.assert_not_called()
