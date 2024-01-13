import requests

ENDPOINT = 'http://localhost:127.0.0.1:8000/posts'


def test_get_posts_by_user():
    response = requests.get(f'{ENDPOINT}/1')
    assert response.status_code == 200


def test_get_post_by_id():
    response = requests.get(f'{ENDPOINT}/1/1')
    assert response.status_code == 200


def test_create_post():
    payload = {
        'title': 'test title',
        'body': 'test body',
        'user_id': 1
    }

    response = requests.post(f'{ENDPOINT}/1', json=payload)
    assert response.status_code == 201


# IMPLEMENT LATER

def test_update_post():
    pass


def test_delete_post():
    pass
