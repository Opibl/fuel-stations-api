from dataclasses import dataclass
from typing import Optional

@dataclass
class Station:
    id: str
    company: str
    address: str
    comuna: str
    region: str
    latitude: float
    longitude: float
    price: Optional[int]
    has_store: bool
    store_name: Optional[str]