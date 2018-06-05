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


def list_ids(p: http.QueryParam) -> dict:
    _auth(p)
    return {'identities': redisclient.get_ids()}


def get_id(p: http.QueryParam, name: str) -> dict:
    _auth(p)
    response = redisclient.get_id(name)
    if response is None:
        raise exceptions.NotFound()
    else:
        return json.loads(response)


def create_id(p: http.QueryParam, name: str, login: str,
              password: str) -> dict:
    _auth(p)
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


def update_id(p: http.QueryParam, name: str, login: http.QueryParam,
              password: http.QueryParam) -> dict:
    _auth(p)
    old_id = redisclient.get_id(name)
    if not old_id:
        raise exceptions.NotFound()
    new_id = json.loads(old_id)
    if not (login or password):
        raise exceptions.BadRequest()
    if login:
        new_id['login'] = login
    if password:
        new_id['password'] = password
    response = redisclient.set_id(name, json.dumps(new_id))
    if not response:
        raise exceptions.HTTPException('Internal error while updating ' +
                                       'identity {}'
                                       .format(name),
                                       500)
    return json.loads(redisclient.get_id(name))


def delete_id(p: http.QueryParam, name: str) -> dict:
    _auth(p)
    response = redisclient.get_id(name)
    if response is None:
        raise exceptions.NotFound()
    if not redisclient.delete_id(name):
        raise exceptions.HTTPException('Internal error while deleting ' +
                                       'identity {}'
                                       .format(name),
                                       500)
    return {'deleted': name}


def _auth(password):
    if not password or not bcrypt.verify(password, config.PASSWORD):
        raise exceptions.Forbidden()
