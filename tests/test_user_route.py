import requests

ENDPOINT = 'http://localhost:127.0.0.1:8000/users'


def test_get_users():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_get_user_by_id():
    response = requests.get(f'{ENDPOINT}/1')
    assert response.status_code == 200


def test_create_user():
    payload = {
        'username': 'TestName',
        'password': '111',
        'age': 90
    }

    response = requests.post(ENDPOINT, json=payload)
    assert response.status_code == 201


# IMPLEMENT LATER

def test_update_user():
    pass


def test_delete_user():
    pass
