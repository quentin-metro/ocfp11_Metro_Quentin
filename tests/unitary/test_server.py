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


@pytest.fixture
def bad_book_fixture(club_fixture):
    bad_book = {
        "club": club_fixture,
        "competition": "Spring Festival"
    }
    return bad_book


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


def test_showSummary_post(client, good_email_fixture):
    response = client.post('/showSummary', data={'email': good_email_fixture})
    assert response.status_code == 200


def test_showSummary_post_incorrect(client, bad_email_fixture):
    response = client.post('/showSummary', data={'email': bad_email_fixture})
    assert response.status_code == 302


def test_book(client, book_fixture):
    competition = book_fixture['competition']
    club = book_fixture['club']
    response = client.get('/book/' + competition + '/' + club + '')
    assert response.status_code == 200
    assert b'<title>Booking for ' + bytes(competition, 'utf-8') + b' || GUDLFT</title>' in response.data


def test_bad_book(client, bad_book_fixture):
    competition = bad_book_fixture['competition']
    club = bad_book_fixture['club']
    response = client.get('/book/' + competition + '/' + club + '')
    assert response.status_code == 200
    assert b'<li>This competition is over</li>' in response.data


def test_no_book(client, bad_book_fixture):
    competition = "no_book"
    club = "no_book"
    response = client.get('/book/' + competition + '/' + club + '')
    assert response.status_code == 200
    assert b'Something went wrong-please try again' in response.data


def test_purchasePlaces(client, book_fixture):
    places = '1'
    response = client.post('/purchasePlaces',
                           data={'club': book_fixture['club'],
                                 'competition': book_fixture['competition'],
                                 'places': places
                                 }
                           )
    assert response.status_code == 307
    response = client.post('/showSummary',
                           data={'club': book_fixture['club'],
                                 'competition': book_fixture['competition'],
                                 'places': places
                                 }
                           )
    assert b'Great-booking complete!' in response.data


def test_purchasePlaces_not_enough(client, book_fixture):
    places = '11'
    response = client.post('/purchasePlaces',
                           data={'club': book_fixture['club'],
                                 'competition': book_fixture['competition'],
                                 'places': places
                                 }
                           )
    assert response.status_code == 307
    response = client.post('/showSummary',
                           data={'club': book_fixture['club'],
                                 'competition': book_fixture['competition'],
                                 'places': places
                                 }
                           )
    assert b'You don&#39;t have enough points available' in response.data


def test_purchasePlaces_too_much(client, book_fixture):
    places = '40'
    response = client.post('/purchasePlaces',
                           data={'club': book_fixture['club'],
                                 'competition': book_fixture['competition'],
                                 'places': places
                                 }
                           )
    assert response.status_code == 307
    response = client.post('/showSummary',
                           data={'club': book_fixture['club'],
                                 'competition': book_fixture['competition'],
                                 'places': places
                                 }
                           )
    assert b'Not enough place available' in response.data


def test_purchasePlaces_bad_time(client, bad_book_fixture):
    places = '40'
    response = client.post('/purchasePlaces',
                           data={'club': bad_book_fixture['club'],
                                 'competition': bad_book_fixture['competition'],
                                 'places': places
                                 }
                           )
    assert response.status_code == 200
    assert b'This competition is over' in response.data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    assert b'You should be redirected automatically to the target URL: <a href="/">/</a>.' in response.data
