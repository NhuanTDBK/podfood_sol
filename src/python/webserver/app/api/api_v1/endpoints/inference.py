import hashlib
import math
from time import time
from typing import Any, List

import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from app import schema
from app.core.config import settings
from app.core.feature_store import feature_store_client
from app.core.model_factory import loader

router = APIRouter()


@router.post(
    "/forecast",
)
def do_forecast(*, input: schema.ListPredictionRequest) -> schema.PredictionOutput:
    """
    Forecast next quantity
    """
    # Load model
    s = time()
    df = feature_store_client.get_features(input.requests)
    model = loader.get_model_by_version(input.model_version)

    res = np.ceil(np.exp(model.predict(df)))

    running_time = time() - s

    return schema.PredictionOutput(
        predictions=res.tolist(),
        metadata=schema.OutputMetadata(response_time=running_time),
    )
