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
