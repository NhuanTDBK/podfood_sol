from typing import List

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    store_id: int
    product_id: int


class ListPredictionRequest(BaseModel):
    requests: List[PredictionRequest]
    model_version: str = "latest"
    predicted_date: str = None
