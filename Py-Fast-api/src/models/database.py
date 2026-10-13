import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("Define MONGO_URI en .env o en las variables de entorno.")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000, connect=False)
db = client.database_apprentice
collection = db.trainee

if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("Conexión exitosa a MongoDB")
    except (ConnectionFailure, ServerSelectionTimeoutError):
        print("No se pudo conectar a MongoDB. Revisa la conexión y la configuración.")
    finally:
        client.close()
