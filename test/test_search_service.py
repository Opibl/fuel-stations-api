import pytest

from app.services.search_service import SearchService
from app.core.exceptions import StationNotFoundException


class MockClient:
    def fetch_stations(self, lat, lng):
        return [
            {
                "id": "1",
                "Compania": "COPEC",
                "Direccion": "Calle 1",
                "Comuna": "Santiago",
                "Region": "RM",
                "Latitud": "-33.4480",
                "Longitud": "-70.6690",
                "Prices": [
                    {
                        "Producto": "Gasolina 93",
                        "Precio": "1500"
                    }
                ],
                "Tienda": {
                    "CodigoTienda": "10",
                    "NombreTienda": "Pronto",
                    "Tipo": "Conveniencia"
                }
            },
            {
                "id": "2",
                "Compania": "SHELL",
                "Direccion": "Calle 2",
                "Comuna": "Santiago",
                "Region": "RM",
                "Latitud": "-33.4490",
                "Longitud": "-70.6700",
                "Prices": [
                    {
                        "Producto": "Gasolina 93",
                        "Precio": "1400"
                    }
                ]
            }
        ]

    def fetch_station_by_id(self, station_id):
        return {
            "Tienda": {
                "CodigoTienda": "10",
                "NombreTienda": "Pronto",
                "Tipo": "Conveniencia"
            }
        }


@pytest.fixture
def service():
    search_service = SearchService()
    search_service.client = MockClient()
    return search_service


def test_find_nearest_station(service):
    result = service.find_station(
        lat=-33.4489,
        lng=-70.6693,
        product="93"
    )

    assert result.success is True
    assert result.data["id"] == "2"


def test_find_cheapest_station(service):
    result = service.find_station(
        lat=-33.4489,
        lng=-70.6693,
        product="93",
        cheapest=True
    )

    assert result.success is True
    assert result.data["precio"] == 1400
    assert result.data["id"] == "2"


def test_find_station_with_store(service):
    result = service.find_station(
        lat=-33.4489,
        lng=-70.6693,
        product="93",
        store=True
    )

    assert result.success is True
    assert result.data["tiene_tienda"] is True
    assert result.data["tienda"] is not None