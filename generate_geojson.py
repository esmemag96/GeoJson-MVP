import requests
import json
import os

# Configuración de Airtable
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = "app10QmnnP1ZfM2Ns"
TABLE_NAME = "Predictions"
API_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# Obtener registros de Airtable
headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
response = requests.get(API_URL, headers=headers)
records = response.json()["records"]

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
with open("predictions.geojson", "w") as file:
    json.dump(geojson, file, indent=2)
