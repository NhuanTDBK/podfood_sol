from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
)
def get_health() -> Any:
    """
    Get Health
    """
    return {"status": "ok"}
