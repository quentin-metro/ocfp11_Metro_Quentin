from tests.conftest import client
import pytest


@pytest.fixture
def good_email_fixture():
    good_email = "admin@irontemple.com"
    return good_email


@pytest.fixture
def club_fixture():
    club = "Iron Temple"
    return club


@pytest.fixture
def competition_fixture():
    competition = "Fall Classic"
    return competition


@pytest.fixture
def book_fixture(club_fixture, competition_fixture):
    book = {
        "club": club_fixture,
        "competition": competition_fixture
    }
    return book


def test_integration_book(client, good_email_fixture, book_fixture):
    """
    Test book from login to logout
    :param client:
    :return:
    """

    # Display index page
    club = book_fixture['club']
    response = client.get('/')
    assert response.status_code == 200
    # assert the number of points for later
    assert bytes(club, 'utf-8') + b' : 4 points.' in response.data

    # Login and check if connect with the good email
    response = client.post('/showSummary', data={'email': good_email_fixture})
    assert response.status_code == 200
    assert b'<h2>Welcome, ' + bytes(good_email_fixture, 'utf-8') + b' </h2>' in response.data
    # assert the number of place for later
    assert b'Number of Places: 13' in response.data

    # Book page  of a competition
    competition = book_fixture['competition']
    response = client.get('/book/' + competition + '/' + club + '')
    assert response.status_code == 200
    assert b'<title>Booking for ' + bytes(competition, 'utf-8') + b' || GUDLFT</title>' in response.data

    # Purchase place for a competition
    places = '1'
    data = {'club': book_fixture['club'],
            'competition': book_fixture['competition'],
            'places': places
            }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 307
    # check if purchase is a success
    response = client.post('/showSummary', data=data)
    assert b'Great-booking complete!' in response.data
    assert b'Number of Places: 12' in response.data
    # Logout
    response = client.get('/logout')
    assert response.status_code == 302
    assert b'You should be redirected automatically to the target URL: <a href="/">/</a>.' in response.data

    # Display index page
    response = client.get('/')
    assert response.status_code == 200
    assert bytes(club, 'utf-8') + b' : 3 points.' in response.data
