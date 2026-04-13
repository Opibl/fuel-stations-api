import requests
from requests.exceptions import RequestException, Timeout

from ..core.config import (
    BENCINA_API_URL,
    REQUEST_TIMEOUT
)


class BencinaClient:

    def fetch_station_by_id(self, station_id: int):
        url = (
            f"{BENCINA_API_URL}"
            f"/estacion_ciudadano/{station_id}"
        )

        try:
            print(
                f"[DETAIL REQUEST] {url}"
            )

            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            print(
                f"[DETAIL STATUS] "
                f"{response.status_code}"
            )

            response.raise_for_status()

            data = response.json()

            return data.get("data", {})

        except Timeout:
            print(
                f"[TIMEOUT] estación "
                f"{station_id}"
            )
            return {}

        except RequestException as e:
            print(
                f"[REQUEST ERROR] "
                f"{station_id}: {e}"
            )
            return {}

        except Exception as e:
            print(
                f"[JSON ERROR] "
                f"{station_id}: {e}"
            )
            return {}

    def fetch_stations(self, lat, lng):
        url = (
            f"{BENCINA_API_URL}"
            f"/busqueda_estacion_filtro"
        )

        params = {
            "latitud": lat,
            "longitud": lng
        }

        try:
            print(
                f"[SEARCH REQUEST] "
                f"{url} {params}"
            )

            response = requests.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT
            )

            print(
                f"[SEARCH STATUS] "
                f"{response.status_code}"
            )

            response.raise_for_status()

            data = response.json()

            return data.get("data", [])

        except Timeout:
            print("[TIMEOUT] búsqueda")
            return []

        except RequestException as e:
            print(
                f"[REQUEST ERROR] "
                f"búsqueda: {e}"
            )
            return []

        except Exception as e:
            print(
                f"[JSON ERROR] "
                f"búsqueda: {e}"
            )
            return []