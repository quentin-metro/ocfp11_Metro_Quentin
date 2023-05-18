from tests.conftest import client
import pytest



@pytest.fixture
def bad_email_fixture():
    bad_email = "incorrect@email.faux"
    return bad_email



def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # assert b"Simply Lift : 13 points." in response.data


def test_index_with_error(client, bad_email_fixture):
    # attempt login with wrong credentials
    response = client.post('/showSummary', data={'email': bad_email_fixture},
                           follow_redirects=True
                           )
    assert response.status_code == 200
    assert b"Sorry, that email wasn&#39;t found." in response.data




def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    assert b'You should be redirected automatically to the target URL: <a href="/">/</a>.' in response.data
