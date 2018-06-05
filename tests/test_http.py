import json
from apistar import test
from app import app
from restpass import redisclient

client = test.TestClient(app)
test_id = {'login': 'supermail@test.com', 'password': '12345'}
password_slug = '?p=password123'


def test_get_ids_list():
    redisclient.set_id('test_id', json.dumps(test_id))
    response = client.get('/ids/'+password_slug)
    assert response.status_code == 200
    assert 'test_id' in response.json()['identities']
    redisclient.delete_id('test_id')


def test_get_existing_id():
    redisclient.set_id('test_id', json.dumps(test_id))
    response = client.get('/ids/test_id' + password_slug)
    assert response.status_code == 200
    assert response.json() == json.loads(json.dumps(test_id))
    redisclient.delete_id('test_id')


def test_get_absent_id():
    redisclient.delete_id('test_id')
    response = client.get('/ids/test_id' + password_slug)
    assert response.status_code == 404


def test_create_existing_id():
    redisclient.set_id('test_id', json.dumps(test_id))
    response = client.post('/ids/test_id' + password_slug +
                           '&login={}'.format(test_id['login']) +
                           '&password={}'.format(test_id['password']))
    assert response.status_code == 500
    redisclient.delete_id('test_id')


def test_create_absent_id():
    response = client.post('/ids/test_id' + password_slug +
                           '&login={}'.format(test_id['login']) +
                           '&password={}'.format(test_id['password']))
    assert response.status_code == 200
    assert(redisclient.get_id('test_id'))
    assert response.json() == {'created': 'test_id'}
    redisclient.delete_id('test_id')


def test_update_existing_id():
    redisclient.set_id('test_id', json.dumps(test_id))
    response = client.put('/ids/test_id' + password_slug +
                          '&login={}'.format('updated'))
    assert response.status_code == 200
    assert response.json() == {'login': 'updated', 'password': '12345'}
    response = client.put('/ids/test_id' + password_slug +
                          '&password={}'.format('updated'))
    assert response.status_code == 200
    assert response.json() == {'login': 'updated', 'password': 'updated'}
    response = client.put('/ids/test_id' + password_slug +
                          '&login={}'.format('again') +
                          '&password={}'.format('again'))
    assert response.status_code == 200
    assert response.json() == {'login': 'again', 'password': 'again'}
    response = client.put('/ids/test_id' + password_slug)
    assert response.status_code == 400
    redisclient.delete_id('test_id')


def test_update_absent_id():
    response = client.put('/ids/test_id' + password_slug +
                          '&password={}'.format('updated'))
    assert response.status_code == 404
    redisclient.delete_id('test_id')


def test_delete_existing_id():
    redisclient.set_id('test_id', json.dumps(test_id))
    response = client.delete('/ids/test_id' + password_slug)
    assert response.status_code == 200
    assert response.json() == {'deleted': 'test_id'}


def test_delete_absent_id():
    response = client.delete('/ids/test_id' + password_slug)
    assert response.status_code == 404
