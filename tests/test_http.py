import json
from apistar import test
from app import app
from restpass import redisclient

client = test.TestClient(app)
id = {'login': 'supermail@test.com', 'password': '12345'}
password_slug = '?pw=password123'


def test_get_ids_list():
    response = client.get('/ids/'+password_slug)
    assert response.status_code == 200
    assert isinstance(response.json()['identities'], list)


def test_get_existing_id():
    redisclient.set_id('test_id', json.dumps(id))
    response = client.get('/ids/test_id'+password_slug)
    assert response.status_code == 200
    assert response.json() == json.loads(json.dumps(id))
    redisclient.delete_id('test_id')


def test_get_absent_id():
    redisclient.delete_id('test_id')
    response = client.get('/ids/test_id'+password_slug)
    assert response.status_code == 404


# TODO
def test_create_id():
    response = client.post('/test_id')
    assert response.status_code == 404
    assert(not redisclient.get_id('test_id'))
    redisclient.delete_id('test_id')


# TODO
def test_update_existing_id():
    redisclient.set_id('test_id', json.dumps(id))
    response = client.put('/ids/test_id'+password_slug)
    assert response.status_code == 404
    redisclient.delete_id('test_id')

# # TODO
# def test_update_absent_id():
#     r.set('test_id', '12345')
#     response = client.put('/ids/test_id')
#     assert response.status_code == 404
#     r.delete('test_id')


# TODO
def test_delete_id():
    redisclient.set_id('test_id', json.dumps(id))
    response = client.delete('/ids/test_id')
    assert response.status_code == 404
    redisclient.delete_id('test_id')
