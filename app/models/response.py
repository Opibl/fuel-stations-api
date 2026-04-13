from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SuccessResponse:
    success: bool = True
    data: Any = None


@dataclass
class ErrorResponse:
    success: bool = False
    error: Optional[str] = None