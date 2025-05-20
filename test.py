
import requests
import json
import time


class Velib:
    def __init__(self, url):
        self.url = url

    def fetch_system_information(self):
        """
        Récupère informations système depuis l'API vélib
        :return: json
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            json_data = response.json()

            system_info = json_data.get("data", {})

            result = {
                "data": {
                    "language": system_info.get("language", ""),
                    "name": system_info.get("name", ""),
                    "system_id": system_info.get("system_id", ""),
                    "timezone": system_info.get("timezone", ""),
                    "url": system_info.get("url", "")
                },
                "lastUpdatedOther": int(time.time()),
                "ttl": json_data.get("ttl", 0)
            }

            return result
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return None

    def fetch_gbfs_feeds(self):
        """
        Récupére et traite des flux GBFS
        :return: json
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            json_data = response.json()

            feeds = json_data.get("data", {}).get("en", {}).get("feeds", [])

            feeds_formatted = [
                {
                    "name": feed.get("name", ""),
                    "url": feed.get("url", "")
                }
                for feed in feeds
            ]

            result = {
                "data": {
                    "en": {
                        "feeds": feeds_formatted
                    }
                },
                "lastUpdatedOther": int(time.time()),
                "ttl": json_data.get("ttl", 0)
            }

            return result
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return None

    def fetch_station_status(self):
        """
        Récupére et traite les données sur l'état actuel des stations d'un système de vélos en libre-service
        :return: json
        """
        response = requests.get(self.url)

        if response.status_code == 200:
            json_data = response.json()

            stations_raw = json_data.get("data", {}).get("stations", [])

            stations_formatted = []
            for station in stations_raw:
                types_list = station.get("num_bikes_available_types", [])
                types = types_list[0] if types_list else {"ebike": 0, "mechanical": 0}

                formatted_station = {
                    "is_installed": station.get("is_installed", 0),
                    "is_renting": station.get("is_renting", 0),
                    "is_returning": station.get("is_returning", 0),
                    "last_reported": station.get("last_reported", 0),
                    "numBikesAvailable": station.get("numBikesAvailable", 0),
                    "numDocksAvailable": station.get("numDocksAvailable", 0),
                    "num_bikes_available": station.get("num_bikes_available", 0),
                    "num_bikes_available_types": [{
                        "ebike": types.get("ebike", 0),
                        "mechanical": types.get("mechanical", 0)
                    }],
                    "num_docks_available": station.get("num_docks_available", 0),
                    "station_id": int(station.get("station_id", 0))
                }
                stations_formatted.append(formatted_station)

            result = {
                "data": {
                    "stations": stations_formatted
                },
                "lastUpdatedOther": int(time.time()),
                "ttl": json_data.get("ttl", 0)
            }

            return result
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return None

velib_system = Velib("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/system_information.json")
info = velib_system.fetch_system_information()
print(json.dumps(info, indent=2, ensure_ascii=False))
velib_status = Velib("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json")
stations = velib_status.fetch_station_status()
