from typing import List, Optional

from pydantic import BaseModel


class OutputMetadata(BaseModel):
    response_time: Optional[int]
    model_version: str = "latest"


class PredictionOutput(BaseModel):
    predictions: List[float]
    low_bound: float = 0.0
    hi_bound: float = 1.0
    metadata: Optional[OutputMetadata]
