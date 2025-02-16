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
        # Validar que las coordenadas existan antes de agregarlas
        if "Longitude" in fields and "Latitude" in fields:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(fields["Longitude"]), float(fields["Latitude"])]
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

    print("modules.geojson generado exitosamente.")

except Exception as e:
    print(f"Error al procesar la respuesta: {e}")
    print("Response text:", response.text)
