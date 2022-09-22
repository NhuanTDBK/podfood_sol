from typing import Any, Dict, List

from app import logger
from app.core.config import settings
from app.db.internal_cache import lru_with_ttl
from app.schema import PredictionRequest
from feast import FeatureStore


class FeatureStoreClient:
    def __init__(self) -> None:
        self.client = FeatureStore(fs_yaml_file=settings.FEAST_CONFIG_URI)
        logger.info("Loading features store")

    @lru_with_ttl()
    def get_feature_service(self, name):
        return self.client.get_feature_service(
            name,
            allow_cache=True,
        )

    def get_features(self, request: List[PredictionRequest]):
        return (
            self.client.get_online_features(
                self.get_feature_service(settings.FEAST_SERVICE_NAME),
                [
                    {
                        "STORE_ID": item.store_id,
                        "PRODUCT_ID": item.product_id,
                    }
                    for item in request
                ],
            )
            .to_df()
            .fillna(0)
        )


feature_store_client = FeatureStoreClient()
