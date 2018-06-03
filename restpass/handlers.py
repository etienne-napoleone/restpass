import json
from apistar import http
from apistar import exceptions
from passlib.hash import bcrypt_sha256 as bcrypt
from restpass import redisclient
from restpass import config


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to restpass, {}!'.format(name)}


def list_ids(pw: http.QueryParam) -> dict:
    if not pw or not bcrypt.verify(pw, config.PASSWORD):
        raise exceptions.Forbidden()
    return {'identities': redisclient.get_ids()}


def get_id(name: str) -> dict:
    response = redisclient.get_id(name)
    if response is None:
        raise exceptions.NotFound()
    else:
        return json.loads(response)


def create_id(name: str, login: str, password: str) -> dict:
    if redisclient.get_id(name):
        raise exceptions.HTTPException('The identity {} already exists'
                                       .format(name),
                                       500)
    response = redisclient.set_id(name, json.dumps({'login': login,
                                                    'password': password}))
    if not response:
        raise exceptions.HTTPException('Internal error while creating ' +
                                       'identity {}'
                                       .format(name),
                                       500)
    return {'created': name}


def update_id(name: str, login: http.QueryParam,
              password: http.QueryParam) -> dict:
    old_id = redisclient.get_id(name)
    new_id = {}
    if not old_id:
        raise exceptions.NotFound()
    if not (login or password):
        raise exceptions.BadRequest()
    if login:
        new_id['login'] = login
    if password:
        new_id['password'] = password
    new_id.setdefault('login', json.loads(old_id)['login'])
    new_id.setdefault('password', json.loads(old_id)['password'])
    response = redisclient.set_id(name, json.dumps(new_id))
    if not response:
        raise exceptions.HTTPException('Internal error while updating ' +
                                       'identity {}'
                                       .format(name),
                                       500)
    return json.loads(redisclient.get_id(name))


def delete_id(name: str) -> dict:
    response = redisclient.get_id(name)
    if response is None:
        raise exceptions.NotFound()
    if not redisclient.delete_id(name):
        raise exceptions.HTTPException('Internal error while deleting ' +
                                       'identity {}'
                                       .format(name),
                                       500)
    return {'deleted': name}
