import redis
from restpass import config

_r = redis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0
)


def get_ids() -> list:
    ids = []
    for item in _r.keys(config.REDIS_PREFIX+'*'):
        ids.append(item[len(config.REDIS_PREFIX):].decode('utf-8'))
    return ids


def get_id(name) -> dict:
    return _r.get(config.REDIS_PREFIX+name)


def set_id(name, value) -> dict:
    return _r.set(config.REDIS_PREFIX+name, value)


# def update_id(name, value) -> dict:
#     return _r.get(config.REDIS_PREFIX+name, value)


def delete_id(name) -> dict:
    return _r.delete(config.REDIS_PREFIX+name)
