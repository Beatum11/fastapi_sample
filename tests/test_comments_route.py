import requests

ENDPOINT = 'http://localhost:127.0.0.1:8000'


def test_get_comments_by_post():
    response = requests.get(f'{ENDPOINT}/1/comments')
    assert response.status_code == 200


def test_create_comment():
    payload = {
        'body': 'test comment',
        'author_id': 1
    }

    response = requests.post(f'{ENDPOINT}/1/1/comments', json=payload)
    assert response.status_code == 201


# IMPLEMENT LATER

def test_update_comment():
    pass


def test_delete_comment():
    pass
