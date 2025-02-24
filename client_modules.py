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
MODULES_TABLE = "Modules"
CLIENTS_TABLE = "Clients"

API_URL_MODULES = f"https://api.airtable.com/v0/{BASE_ID}/{MODULES_TABLE}"
API_URL_CLIENTS = f"https://api.airtable.com/v0/{BASE_ID}/{CLIENTS_TABLE}"

# Obtener registros de Airtable
headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

def fetch_airtable_data(url):
    """ Función para obtener datos desde Airtable """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("records", [])
    else:
        print(f"❌ Error obteniendo datos desde {url}: {response.text}")
        return []

# ✅ 1. Obtener todos los clientes
clients_data = fetch_airtable_data(API_URL_CLIENTS)

# 🏷️ Especificar el nombre del cliente para filtrar
CLIENT_NAME = "Cruz Roja Española"  # 👈 Cambia esto según el cliente que deseas visualizar

# Buscar el cliente y obtener los módulos asignados
client_modules_ids = []
client_info = {}

for client in clients_data:
    fields = client["fields"]
    if fields.get("Name") == CLIENT_NAME:  # 🟢 Buscar cliente por nombre
        client_info = {
            "client_name": fields.get("Name", "Desconocido"),
            "country": fields.get("Country", "N/A"),
            "organization": fields.get("Organization", "N/A"),
        }
        client_modules_ids = fields.get("Assigned Modules", [])  # 🔍 Obtener los módulos asignados
        break  # 🔹 Solo necesitamos un cliente, así que terminamos aquí

# Si no encontramos el cliente, detener ejecución
if not client_modules_ids:
    print(f"⚠️ No se encontraron módulos asignados para el cliente: {CLIENT_NAME}")
    exit(1)

print(f"✅ Cliente encontrado: {client_info['client_name']}, con {len(client_modules_ids)} módulos asignados.")

# ✅ 2. Obtener los módulos desde Airtable
modules_data = fetch_airtable_data(API_URL_MODULES)

# 📌 Depuración: Listar IDs de módulos en ambas listas
module_ids_from_airtable = [record["id"] for record in modules_data]

# Crear el GeoJSON solo con los módulos del cliente
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for record in modules_data:
    # module_id = record["id"]  # El ID real del módulo en Airtable
    fields = record["fields"]
    module_id = str(fields.get("ID"))
    # 📌 Depuración: Mostrar coincidencias encontradas
    if module_id in client_modules_ids:

        longitude = float(fields["Longitude"])
        latitude = float(fields["Latitude"])

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
                "ocuppancy": fields.get("Ocuppancy", "N/A"),
                "men": fields.get("Men", 0),
                "women": fields.get("Women", 0),
                "children": fields.get("Children", 0),
                "camp": fields.get("Name (from Settlements) (from Camp)", "N/A"),
                "installation_date": fields.get("Installation Date", "N/A"),
                "last_maintenance": fields.get("Last Maintenance Date", "N/A"),
                "next_maintenance": fields.get("Next Maintenance Date", "N/A"),
                "client_name": client_info["client_name"],
                "client_country": client_info["country"],
                "client_organization": client_info["organization"],
            }
        }
        geojson["features"].append(feature)

# 📌 Depuración final: Mostrar cuántos módulos se encontraron
print(f"✅ Módulos filtrados: {len(geojson['features'])} módulos encontrados para {CLIENT_NAME}")

# Guardar el archivo filtered_modules.geojson
with open("filtered_modules.geojson", "w") as file:
    json.dump(geojson, file, indent=2)

print(f"✅ filtered_modules.geojson generado exitosamente con {len(geojson['features'])} módulos.")