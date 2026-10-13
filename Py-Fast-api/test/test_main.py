import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# URI de conexión a MongoDB Atlas
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("Define la variable de entorno MONGO_URI antes de ejecutar este archivo.")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

#Crear o seleccionar la base de datos y la colección
db = client["Fast-API-ENV"]
collection = db["703-Environment"]

#crear model de datos para la coleccion
Environment_new_data = {
    "id":3,
    "name":"Joan Santiago",
    "status": "Dead",
    "species": "Human",
    "gender": "Male",
}


try:
    # Verificar la conexión
    client.admin.command("ping")
    print("Conexión exitosa a MongoDB")
    #insertar el modelo de datos en la coleccion
    collection.insert_one(Environment_new_data)
    print("Documento insetado en la colección '703-Environment' en la base de datos 'Fast-API-ENV'")

except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"Error al conectar a MongoDB: {e}")

finally:
    # Cerrar la conexión 
    client.close()