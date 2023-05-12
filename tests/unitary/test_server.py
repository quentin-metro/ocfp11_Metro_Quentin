from tests.conftest import client



def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_with_error(client):
    # attempt login with wrong credentials
    response = client.post('/showSummary', data={'email': 'incorrect@email.faux'},
                           follow_redirects=True
                           )
    assert response.status_code == 200
    assert b"Sorry, that email wasn&#39;t found." in response.data


def test_index_post(client):
    email = "admin@irontemple.com"
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200


def test_index_post_incorrect(client):
    email = "incorrect@email.faux"
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 302
