from app.models import station

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
        stations = self.client.fetch_stations(lat, lng)
        candidates = []

        for station in stations:
            price = self._get_product_price(
                station,
                product
            )

            if price is None:
                continue

            try:
                station_lat = float(
                    str(
                        station.get("latitud")
                        or station.get("Latitud")
                    ).replace(",", ".")
                )

                station_lng = float(
                    str(
                        station.get("longitud")
                        or station.get("Longitud")
                    ).replace(",", ".")
                )

            except (
                ValueError,
                TypeError,
                KeyError
            ):
                continue

            distance = (
                self.distance_service.haversine(
                    lat,
                    lng,
                    station_lat,
                    station_lng
                )
            )

            candidates.append({
                "raw": station,
                "id": str(
                    station.get("id")
                    or station.get("CodEs")
                ),
                "precio": price,
                "latitud": station_lat,
                "longitud": station_lng,
                "distancia_lineal": round(
                    distance,
                    2
                )
            })

        if not candidates:
            raise StationNotFoundException(
                "No se encontraron estaciones "
                "para el producto solicitado"
            )

        
        candidates.sort(
            key=lambda x: x[
                "distancia_lineal"
            ]
        )

        
        nearest_candidates = candidates[:5]

        filtered = []

        for item in nearest_candidates:
            station = item["raw"]
            detail = station

            
            try:
                detail = self.client.fetch_station_by_id(
                    item["id"]
                )
            except Exception as e:
                print(
                    f"Error detalle "
                    f"{item['id']}: {e}"
                )

            
            has_store = self._has_store(detail)
            store_data = self._get_store_data(detail)

            
            if store and not has_store:
                continue

            filtered.append({
                "id": item["id"],
                "compania": self._get_company_name(
                    detail
                ),
                "direccion": (
                    detail.get("direccion")
                    or detail.get("Direccion")
                    or station.get("direccion")
                    or station.get("Direccion")
                ),
                "comuna": (
                    detail.get("comuna")
                    or detail.get("Comuna")
                    or station.get("comuna")
                    or station.get("Comuna")
                ),
                "region": (
                    detail.get("region")
                    or detail.get("Region")
                    or station.get("region")
                    or station.get("Region")
                ),
                "latitud": item["latitud"],
                "longitud": item["longitud"],
                "distancia_lineal": item[
                    "distancia_lineal"
                ],
                "precio": item["precio"],
                "tiene_tienda": has_store,
                "tienda": store_data
            })

        if not filtered:
            raise StationNotFoundException(
                "No se encontraron estaciones "
                "con los filtros dados"
            )

        result = (
            self._select_best_station(
                filtered,
                cheapest
            )
        )

        return SuccessResponse(
            data=result
        )

    def _get_product_price(
        self,
        station,
        product
    ):
        combustibles = station.get(
            "combustibles",
            []
        )

        prices = station.get(
            "Prices",
            []
        )

        product_map = {
            "93": [
                "93",
                "Gasolina 93"
            ],
            "95": [
                "95",
                "Gasolina 95"
            ],
            "97": [
                "97",
                "Gasolina 97"
            ],
            "diesel": [
                "DI",
                "Diesel"
            ],
            "kerosene": [
                "KE",
                "Kerosene"
            ]
        }

        targets = product_map.get(
            product.lower()
        )

        if not targets:
            return None

        for fuel in combustibles:
            if (
                fuel.get(
                    "nombre_corto"
                )
                in targets
            ):
                try:
                    return int(
                        float(
                            str(
                                fuel.get(
                                    "precio"
                                )
                            ).replace(
                                ",",
                                "."
                            )
                        )
                    )
                except (
                    ValueError,
                    TypeError
                ):
                    return None

        for fuel in prices:
            if (
                fuel.get(
                    "Producto"
                )
                in targets
            ):
                try:
                    return int(
                        float(
                            str(
                                fuel.get(
                                    "Precio"
                                )
                            ).replace(
                                ",",
                                "."
                            )
                        )
                    )
                except (
                    ValueError,
                    TypeError
                ):
                    return None

        return None

    def _has_store(
        self,
        station
    ):
        if (
            station.get("Tienda")
            or station.get(
                "tienda"
            )
        ):
            return True

        services = station.get(
            "Servicios"
        )

        if isinstance(
            services,
            dict
        ):
            codes = services.get(
                "CodSer",
                []
            )

            if 4 in codes:
                return True

        services = station.get(
            "servicios",
            []
        )

        for service in services:
            if isinstance(
                service,
                dict
            ):
                name = (
                    service.get(
                        "nombre"
                    )
                    or service.get(
                        "Nombre"
                    )
                    or ""
                ).lower()

                keywords = [
                    "tienda",
                    "pronto",
                    "upa",
                    "select",
                    "market",
                    "shop"
                ]

                if any(
                    k in name
                    for k in keywords
                ):
                    return True

        return False

    def _get_store_data(self, station):
        store = (
            station.get("Tienda")
            or station.get("tienda")
        )

        if store:
            return {
                "codigo": (
                    store.get("CodigoTienda")
                    or store.get("codigo")
                ),
                "nombre": (
                    store.get("NombreTienda")
                    or store.get("nombre")
                ),
                "tipo": (
                    store.get("Tipo")
                    or store.get("tipo")
                )
            }

        services = station.get(
            "servicios",
            []
        )

        for service in services:
            if not isinstance(service, dict):
                continue

            name = str(
                service.get("nombre")
                or service.get("Nombre")
                or ""
            )

            if "tienda" in name.lower():
                return {
                    "codigo": str(
                        service.get("id")
                    ),
                    "nombre": name,
                    "tipo": "Conveniencia"
                }

        return None

    def _get_company_name(self, station):
        brand_code = station.get("marca")

        brand_map = {
            4: "SHELL",
            5: "COPEC",
            151: "ARAMCO"
        }

        if brand_code in brand_map:
            return brand_map[brand_code]

        logo_url = str(
            station.get("logo")
            or ""
        ).lower()

        if "shell" in logo_url:
            return "SHELL"
        elif "aramco" in logo_url:
            return "ARAMCO"
        elif "copec" in logo_url:
            return "COPEC"
        elif "logo5" in logo_url:
            return "COPEC"

        return f"Marca {brand_code}"

    def _select_best_station(
        self,
        stations,
        cheapest
    ):
        if cheapest:
            min_price = min(
                station["precio"]
                for station
                in stations
            )

            stations = [
                station
                for station
                in stations
                if (
                    station["precio"]
                    == min_price
                )
            ]

        return min(
            stations,
            key=lambda x: x[
                "distancia_lineal"
            ]
        )