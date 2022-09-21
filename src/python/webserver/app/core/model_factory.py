from typing import Dict

import mlflow

from app import logger
from app.core.config import settings


class ModelLoader:
    def __init__(self, mlflow_uri: str = None, model_name: str = None) -> None:
        self.mlflow_uri = mlflow_uri or settings.MLFLOW_URI
        self.model_name = model_name or settings.MODEL_REGISTRY_NAME

        self.mlflow_client = mlflow.MlflowClient(tracking_uri=self.mlflow_uri)
        mlflow.set_tracking_uri(settings.MLFLOW_URI)
        mlflow.set_registry_uri(settings.MLFLOW_URI)

        self._mapper_: Dict = {}

        logger.info("Loading model")

    def _load_model(self, version: str = None):
        # model_uri = f"models:/{self.model_name}/{version}"
        model_version = self.mlflow_client.get_model_version(
            self.model_name, version=version
        )
        model_uri = model_version.source

        model = mlflow.pyfunc.load_model(model_uri=model_uri)

        return model

    def register_model(self, version: str = "latest"):
        """
        Load latest by default
        """
        version_query = version
        if version == "latest":
            list_model_version_info = self.mlflow_client.get_latest_versions(
                self.model_name,
                stages=["Production"],
            )
            if list_model_version_info:
                version_query = list_model_version_info[-1].version

        model = self._load_model(version=version_query)

        self._mapper_[version_query] = model
        self._mapper_[version] = model

        return self

    def unregister_model(self, version: str = None):
        del self._mapper_[version]
        return self

    def get_model_by_version(self, version: str = "latest"):
        if version not in self._mapper_:
            self.register_model(version)

        return self._mapper_[version]


loader = ModelLoader()
