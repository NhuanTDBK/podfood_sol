import redis

from app.core.config import settings


def get_redis() -> redis.client.Redis:
    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        db=0,
        socket_timeout=5,
    )
    ping = client.ping()
    if ping is True:
        return client
