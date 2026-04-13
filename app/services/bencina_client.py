import requests
from ..core.config import BENCINA_API_URL, REQUEST_TIMEOUT


class BencinaClient:

    def fetch_station_by_id(self, station_id: int):
        url = f"{BENCINA_API_URL}/estacion_ciudadano/{station_id}"

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()["data"]

    def fetch_stations(self):
        stations = []

        # rango dinámico de estaciones consultadas
        start_id = 1500
        end_id = 2000

        for station_id in range(start_id, end_id + 1):
            try:
                station = self.fetch_station_by_id(station_id)
                stations.append(station)
            except requests.RequestException:
                continue
            except KeyError:
                continue

        return stations