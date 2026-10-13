from pumongo import MongoCLient
from pymongo.errors import ConnectionFailure, SrverSelectionTimeoutError

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI, ServerSelectionTimeoutMS = 3000)

db = client.database_apprentice
collection =db.trainee

try:
    client.server_info()
    client.admin.command("ping")
    print("Conexión exitosa a MongoDB")

except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"Error al conectar a MongoDB: [e]")
finally:
    client.close()