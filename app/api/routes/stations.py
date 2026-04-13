from fastapi import APIRouter, Query, HTTPException
from ...services.search_service import SearchService
from ...core.exceptions import StationNotFoundException

router = APIRouter()
search_service = SearchService()


@router.get("/search")
def search_station(
    lat: float = Query(...),
    lng: float = Query(...),
    product: str = Query(...),
    nearest: bool = Query(True),
    store: bool = Query(False),
    cheapest: bool = Query(False)
):
    try:
        response = search_service.find_station(
            lat=lat,
            lng=lng,
            product=product,
            nearest=nearest,
            store=store,
            cheapest=cheapest
        )

        return response.__dict__

    except StationNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )