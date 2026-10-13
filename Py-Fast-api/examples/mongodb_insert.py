import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


def main():
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise RuntimeError(
            "Define la variable de entorno MONGO_URI antes de ejecutar este archivo."
        )

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    db = client["Fast-API-ENV"]
    collection = db["703-Environment"]

    Environment_new_data = {
        "id": 3,
        "name": "Joan Santiago",
        "status": "Dead",
        "species": "Human",
        "gender": "Male",
    }

    try:
        client.admin.command("ping")
        print("Conexión exitosa a MongoDB")
        collection.insert_one(Environment_new_data)
        print(
            "Documento insetado en la colección '703-Environment' en la base de datos 'Fast-API-ENV'"
        )

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"Error al conectar a MongoDB: {e}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
