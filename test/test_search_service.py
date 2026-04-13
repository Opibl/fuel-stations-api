from app.services.distance_service import DistanceService


def test_haversine_distance():
    distance = DistanceService.haversine(
        -33.4463,
        -70.6427,
        -33.4464,
        -70.6428
    )

    assert distance >= 0