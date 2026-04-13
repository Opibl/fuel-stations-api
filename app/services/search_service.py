from .bencina_client import BencinaClient
from .distance_service import DistanceService
from ..models.response import SuccessResponse
from ..core.exceptions import StationNotFoundException


class SearchService:

    def __init__(self):
        self.client = BencinaClient()
        self.distance_service = DistanceService()

    def find_station(
        self,
        lat,
        lng,
        product,
        nearest=True,
        store=False,
        cheapest=False
    ):
        stations = self.client.fetch_stations()
        filtered = []

        for station in stations:
            price = self._get_product_price(station, product)

            if price is None:
                continue

            has_store = self._has_store(station)

            if store and not has_store:
                continue

            distance = self.distance_service.haversine(
                lat,
                lng,
                float(station["latitud"]),
                float(station["longitud"])
            )

            filtered.append({
                "id": str(station["id"]),
                "compania": self._get_company_name(station),
                "direccion": station["direccion"],
                "comuna": station["comuna"],
                "region": station["region"],
                "latitud": float(station["latitud"]),
                "longitud": float(station["longitud"]),
                "distancia_lineal": distance,
                "precio": price,
                "tiene_tienda": has_store,
                "tienda": self._get_store_data(station)
            })

        if not filtered:
            raise StationNotFoundException(
                "No se encontraron estaciones para los filtros dados"
            )

        result = self._select_best_station(
            filtered,
            cheapest
        )

        return SuccessResponse(data=result)

    def _get_product_price(self, station, product):
        combustibles = station.get("combustibles", [])

        product_map = {
            "93": "93",
            "95": "95",
            "97": "97",
            "diesel": "DI",
            "kerosene": "KE"
        }

        target = product_map.get(product.lower())

        if not target:
            return None

        for fuel in combustibles:
            if fuel["nombre_corto"] == target:
                return int(float(fuel["precio"]))

        return None

    def _has_store(self, station):
        services = station.get("servicios", [])

        return any(
            "tienda" in service["nombre"].lower()
            for service in services
        )

    def _get_store_data(self, station):
        services = station.get("servicios", [])

        for service in services:
            if "tienda" in service["nombre"].lower():
                return {
                    "codigo": service["id"],
                    "nombre": service["nombre"],
                    "tipo": "Conveniencia"
                }

        return None

    def _get_company_name(self, station):
        logo_url = station.get("logo", "").lower()

        if "copec" in logo_url:
            return "COPEC"
        elif "shell" in logo_url:
            return "SHELL"
        elif "aramco" in logo_url:
            return "ARAMCO"

        return "Sin marca"

    def _select_best_station(self, stations, cheapest):
        if cheapest:
            min_price = min(
                station["precio"]
                for station in stations
            )

            stations = [
                station
                for station in stations
                if station["precio"] == min_price
            ]

        return min(
            stations,
            key=lambda x: x["distancia_lineal"]
        )