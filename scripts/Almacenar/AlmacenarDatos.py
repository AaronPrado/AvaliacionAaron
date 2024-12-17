import requests
import time
import pymongo
from pymongo import MongoClient

endpoint = "http://api.citybik.es/v2/networks/bicicorunha"
intervalo_tiempo = 1
MONGO_URI = "mongodb://mongo:27017/"
DB_NOMBRE = "CityBikes"
COL_NOMBRE = "Corunha"

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
        return data.get("network", {}).get("stations", [])
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