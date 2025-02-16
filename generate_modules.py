import requests
import json
import os

# Configuración de Airtable
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
if AIRTABLE_API_KEY:
    print("API Key encontrada.")
else:
    print("API Key no encontrada.")
BASE_ID = "app10QmnnP1ZfM2Ns"
TABLE_NAME = "Modules"
API_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# Obtener registros de Airtable
headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
response = requests.get(API_URL, headers=headers)
##records = response.json()["records"]

try:
    response_data = response.json()
    if "records" not in response_data:
        print("Error: No records found in the response.")
        print("Response:", response_data)
        exit(1)

    records = response_data["records"]

    # Crear el GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for record in records:
        fields = record["fields"]

        # Filtrar solo los registros con status "In use"
        if fields.get("Status") == "In use":
            # Validar que las coordenadas existan y sean convertibles
            if "Longitude" in fields and "Latitude" in fields:
                try:
                    # Reemplazar comas con puntos y convertir a float
                    longitude = float(fields["Longitude"].replace(",", "."))
                    latitude = float(fields["Latitude"].replace(",", "."))
                except ValueError:
                    print(f"Coordenadas inválidas para el registro: {fields}")
                    continue

                # Crear la estructura GeoJSON
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    },
                    "properties": {
                        "id": fields.get("ID", "N/A"),
                        "type": fields.get("Type", "N/A"),
                        "status": fields.get("Status", "N/A"),
                        "capacity": fields.get("Capacity", "N/A"),
                        "camp": fields.get("Name (from Settlements) (from Camp)", "N/A"),
                        "client": fields.get("Name (from Cliente", {}).get("asent.)", "N/A"),
                        "installation_date": fields.get("Installation Date", "N/A"),
                        "last_maintenance": fields.get("Last Mantainance Date", "N/A")
                    }
                }
                geojson["features"].append(feature)

    # Guardar el archivo modules.geojson
    with open("modules.geojson", "w") as file:
        json.dump(geojson, file, indent=2)

    print("modules.geojson generado exitosamente con registros 'In use'.")

except Exception as e:
    print(f"Error al procesar la respuesta: {e}")
    print("Response text:", response.text)
