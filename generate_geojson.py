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
TABLE_NAME = "Predictions"
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
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [fields["Location Longitude"], fields["Location Latitude"]]
            },
            "properties": {
                "forecast_date": fields["Forecast Date"],
                "city": fields["Location City"],
                "country": fields["Location Country"],
                "risk_level": fields["Risk Level"],
                "event_description": fields["Event Description"],
                "estimated_migrants": fields["Estimated Migrants"],
                "modules_needed": fields["Modules Needed"],
                "logistics_route": fields["Logistics Route"]
            }
        }
        geojson["features"].append(feature)

    # Guardar el archivo GeoJSON
    with open("data.geojson", "w") as file:
        json.dump(geojson, file, indent=2)

    print("GeoJSON generado exitosamente.")

except Exception as e:
    print(f"Error al procesar la respuesta: {e}")
    print("Response text:", response.text)
