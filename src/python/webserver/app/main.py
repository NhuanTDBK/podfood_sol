from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.router import api_router
from app.core.config import settings

# setup loggers
# logging.config.fileConfig('logging.conf', disable_existing_loggers=True)

# # get root logger
# logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.
#                                       # This will get the root logger since no logger in the configuration has this name.

# logger.info("Start server")
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)


app.include_router(api_router, prefix=settings.API_V1_STR)

Instrumentator().instrument(app).expose(app)
