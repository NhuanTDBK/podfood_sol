from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "prod"
    PROJECT_NAME = "forecast"
    MODEL_REGISTRY_NAME: str = "QuantityPredictor"
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str
    ALGORITHM: str = "SHA1"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 365
    MLFLOW_URI = "http://0.0.0.0:5001"

    REDIS_HOST = "0.0.0.0"
    REDIS_PORT = 6379

    FEAST_CONFIG_URI = "./feature_store.yaml"
    FEAST_SERVICE_NAME = "quantity_fs"
    MLFLOW_S3_ENDPOINT_URL = "http://s3-faker:4569"
    AWS_ACCESS_KEY_ID = 12
    AWS_SECRET_ACCESS_KEY = 12
    AWS_DEFAULT_REGION = "asia"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
