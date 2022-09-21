from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
)
def get_model_versions() -> Any:
    """
    Get Health
    """
    return {"status": "ok"}
