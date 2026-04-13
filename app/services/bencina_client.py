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
        station_ids = [
            1554,
            1555,
            1556,
            1557,
            1558,
            1559
        ]

        stations = []

        for station_id in station_ids:
            try:
                station = self.fetch_station_by_id(station_id)
                stations.append(station)
            except Exception:
                continue

        return stations