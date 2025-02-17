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
SETTLEMENTS_TABLE = "Settlements"  # Nombre de la tabla de Settlements
CAMPS_TABLE = "Camps"  # Nombre de la tabla de Camps

# Función para obtener datos desde Airtable
def fetch_airtable_data(table_name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "records" not in data:
        print(f"Error: No records found in {table_name}")
        return []
    
    return data["records"]
# Función para obtener datos de Airtable
def fetch_airtable_data(api_url):
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return data.get("records", [])

# Obtener datos de Settlements y Camps
settlements_data = fetch_airtable_data(API_URL_SETTLEMENTS)
camps_data = fetch_airtable_data(API_URL_CAMPS)

# Crear un diccionario con los datos de Camps para acceso rápido
camps_dict = {}
for camp in camps_data:
    fields = camp["fields"]
    camp_id = str(fields.get("ID", "")).strip()  # Convertimos el ID en string limpio

    camps_dict[camp_id] = {
        "camp_name": fields.get("Name", "Desconocido"),
        "clients": fields.get("Clients", "Sin clientes"),
        "modules_count": fields.get("Recuento (Modules)", "0"),
    }

# Crear el GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Procesar Settlements y unir datos de Camps
for record in settlements_data:
    fields = record["fields"]
    
    if "Longitude" in fields and "Latitude" in fields:
        try:
            longitude = float(fields["Longitude"])
            latitude = float(fields["Latitude"])
        except ValueError:
            print(f"Error en coordenadas para {fields.get('Name', 'N/A')}: {fields['Latitude']}, {fields['Longitude']}")
            continue

        camp_id = str(fields.get("Camps", "")).strip()  # ID del campamento
        
        # Datos del campamento correspondiente
        camp_info = camps_dict.get(camp_id, {
            "camp_name": "No asignado",
            "clients": "Desconocido",
            "modules_count": "0"
        })

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "properties": {
                "id": fields.get("ID", "N/A"),
                "settlement_name": fields.get("Name", "N/A"),
                "clients": camp_info["clients"],
                "modules_count": camp_info["modules_count"],
                "camp_name": camp_info["camp_name"],
            }
        }
        geojson["features"].append(feature)

# Guardar el archivo settlements.geojson
with open("settlements.geojson", "w", encoding="utf-8") as file:
    json.dump(geojson, file, indent=2, ensure_ascii=False)

print("✅ settlements.geojson generado exitosamente.")