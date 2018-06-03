import json
from apistar import http
from apistar import exceptions
from passlib.hash import bcrypt_sha256 as bcrypt
from restpass import redisclient
from restpass import config


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, {}!'.format(name)}


def list_ids(pw: http.QueryParam) -> dict:
    if not pw or not bcrypt.verify(pw, config.PASSWORD):
        raise exceptions.Forbidden()
    return {'identities': redisclient.get_ids()}


def get_id(name: str) -> dict:
    value = redisclient.get_id(name)
    if value is None:
        raise exceptions.NotFound()
    else:
        return json.loads(value)


def create_id(name: str) -> dict:
    raise exceptions.MethodNotAllowed()


def update_id(name: str) -> dict:
    raise exceptions.MethodNotAllowed()


def delete_id(name: str) -> dict:
    value = redisclient.get_id(name)
    if value is None:
        raise exceptions.NotFound()
    if not redisclient.delete_id(name):
        raise exceptions.HTTPException('Internal Server Error', 500)
    return {'deleted': name}
