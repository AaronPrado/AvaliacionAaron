import pymongo
import pandas as pd
from datetime import datetime
import os  

MONGO_URI = "mongodb://localhost:27017/"  
DATABASE_NAME = "SpaceStation" 
COLLECTION_NAME = "Estacion" 

FIELDS_TO_EXPORT = ["latitude", "longitud"]

def export_data():
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        cursor = collection.find({}, {field: 1 for field in FIELDS_TO_EXPORT})

        data = list(cursor)

        if not data:
            print("No se encontraron documentos en la base de datos.")
            return

        df = pd.DataFrame(data)

        df["_id"] = df["_id"].astype(str)

        script_directory = os.path.dirname(os.path.abspath(__file__))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"exported_data_{timestamp}"

        csv_filename = os.path.join(script_directory, f"{base_filename}.csv")
        parquet_filename = os.path.join(script_directory, f"{base_filename}.parquet")

        df.to_csv(csv_filename, index=False)
        print(f"Datos exportados a CSV: {csv_filename}")

        df.to_parquet(parquet_filename, index=False)
        print(f"Datos exportados a Parquet: {parquet_filename}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

export_data()