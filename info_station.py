
import requests
import csv
import tempfile
import os
import time
from google.cloud import bigquery

# === Configuration ===
SERVICE_ACCOUNT_JSON = r"C:\HETIC\2024-2025\Data_api_web\velib-460309-e9d68bc94c87.json"
PROJECT_ID = "velib-460309"
DATASET_ID = "velib_dataset"
INFO_TABLE_ID = "station_information"

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

def fetch_station_information():
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        stations_raw = json_data.get("data", {}).get("stations", [])

        stations_formatted = []
        for station in stations_raw:
            stations_formatted.append({
                "station_id": int(station.get("station_id", 0)),
                "name": station.get("name", ""),
                "address": station.get("address", ""),
                "lat": station.get("lat", 0.0),
                "lon": station.get("lon", 0.0),
                "capacity": station.get("capacity", 0),
            })

        return stations_formatted
    else:
        raise Exception(f"Erreur de requête : {response.status_code}")

def save_to_temp_csv(data, fieldnames):
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", newline="", encoding="utf-8")
    writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    temp_file.close()
    return temp_file.name

def load_csv_to_bigquery(csv_file_path, dataset_id, table_id):
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # ou WRITE_APPEND
    )

    with open(csv_file_path, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
        load_job.result()  # Attendre que le job se termine

    print(f"✅ Données chargées avec succès dans {table_id}")
    os.remove(csv_file_path)

if __name__ == "__main__":
    print("⏳ Récupération des données...")
    stations = fetch_station_information()

    print("💾 Sauvegarde dans un fichier CSV temporaire...")
    csv_path = save_to_temp_csv(stations, ["station_id", "name", "address", "lat", "lon", "capacity"])

    print("🚀 Chargement dans BigQuery...")
    load_csv_to_bigquery(csv_path, DATASET_ID, INFO_TABLE_ID)
