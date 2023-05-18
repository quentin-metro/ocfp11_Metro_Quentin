from tests.conftest import client
import pytest


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
