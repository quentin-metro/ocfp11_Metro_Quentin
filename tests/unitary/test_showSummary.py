from tests.conftest import client
import pytest


@pytest.fixture
def good_email_fixture():
    good_email = "admin@irontemple.com"
    return good_email


@pytest.fixture
def bad_email_fixture():
    bad_email = "incorrect@email.faux"
    return bad_email


def test_showSummary_post(client, good_email_fixture):
    response = client.post('/showSummary', data={'email': good_email_fixture})
    assert response.status_code == 200


def test_showSummary_post_incorrect(client, bad_email_fixture):
    response = client.post('/showSummary', data={'email': bad_email_fixture})
    assert response.status_code == 302
