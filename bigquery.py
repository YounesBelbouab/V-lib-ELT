import csv
import os
from dagster import asset
import requests
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

SERVICE_ACCOUNT_JSON = r"C:\HETIC\2024-2025\Data_api_web\velib-460309-e9d68bc94c87.json"
PROJECT_ID = "velib-460309"
DATASET_ID = "velib_dataset"
TABLE_ID = "station_status"

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)


@asset
def fetch_and_load_velib_station_status():
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la récupération des données: {response.status_code}")

    json_data = response.json()
    stations_raw = json_data.get("data", {}).get("stations", [])

    stations_formatted = []
    for station in stations_raw:
        types_list = station.get("num_bikes_available_types", [])
        types = types_list[0] if types_list else {"ebike": 0, "mechanical": 0}

        stations_formatted.append({
            "station_id": int(station.get("station_id", 0)),
            "is_installed": station.get("is_installed", 0),
            "is_renting": station.get("is_renting", 0),
            "is_returning": station.get("is_returning", 0),
            "last_reported": station.get("last_reported", 0),
            "num_bikes_available": station.get("num_bikes_available", 0),
            "ebike": types.get("ebike", 0),
            "mechanical": types.get("mechanical", 0),
            "num_docks_available": station.get("num_docks_available", 0),
        })

    # Création table si absente
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(TABLE_ID)
    try:
        client.get_table(table_ref)
    except NotFound:
        schema = [
            bigquery.SchemaField("station_id", "INTEGER"),
            bigquery.SchemaField("is_installed", "INTEGER"),
            bigquery.SchemaField("is_renting", "INTEGER"),
            bigquery.SchemaField("is_returning", "INTEGER"),
            bigquery.SchemaField("last_reported", "INTEGER"),
            bigquery.SchemaField("num_bikes_available", "INTEGER"),
            bigquery.SchemaField("ebike", "INTEGER"),
            bigquery.SchemaField("mechanical", "INTEGER"),
            bigquery.SchemaField("num_docks_available", "INTEGER"),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)

    # Écrire en CSV temporaire
    temp_file_path = "stations_temp.csv"
    with open(temp_file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=stations_formatted[0].keys())
        writer.writeheader()
        writer.writerows(stations_formatted)

    # Charger dans BigQuery
    with open(temp_file_path, "rb") as source_file:
        job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=False)
        load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
        load_job.result()  # Attendre fin de l'upload

    os.remove(temp_file_path)  # Nettoyage fichier temporaire

    return f"{len(stations_formatted)} lignes chargées dans BigQuery (via fichier CSV)."

#stoquer ds un bucket bigquery, data-transfer


if __name__ == "__main__":
    result = fetch_and_load_velib_station_status()
    print(result)
