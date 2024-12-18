import requests
import time
import pymongo
from pymongo import MongoClient

endpoint = "http://api.open-notify.org/iss-now.json"
intervalo_tiempo = 3
MONGO_URI = "mongodb://localhost:27017/"
DB_NOMBRE = "SpaceStation"
COL_NOMBRE = "Estacion"

def mongo_connect():
    cliente = MongoClient(MONGO_URI)
    db = cliente[DB_NOMBRE]
    coleccion = db[COL_NOMBRE]
    return coleccion

def fetch_data():

    try:
        response = requests.get(endpoint)
        response.raise_for_status() 
        
        data = response.json()
        
        iss_position = data.get("iss_position", {})
        
        return iss_position if iss_position else None
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

def mongo_update(coleccion, data):

    if data:
        try:
            if isinstance(data, list):
                coleccion.insert_many(data)
            else:
                coleccion.insert_one(data)
            print("Datos almacenados correctamente en MongoDB.")
        except pymongo.errors.PyMongoError as e:
            print(f"Error al almacenar datos en MongoDB: {e}")

coleccion = mongo_connect()
print("Conexión a MongoDB establecida.")

try:
    while True:
        print("Obteniendo datos de la API...")
        data = fetch_data()
        if data:
            mongo_update(coleccion, data)
        else:
            print("No se recibieron datos para almacenar.")
        print(f"Esperando {intervalo_tiempo} minutos para la próxima ejecución...\n")
        time.sleep(intervalo_tiempo * 60)  # Espera el tiempo especificado en segundos
except KeyboardInterrupt:
    print("Script detenido por el usuario.")