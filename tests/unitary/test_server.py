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


def test_showSummary_post(client):
    email = "admin@irontemple.com"
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200


def test_showSummary_post_incorrect(client):
    email = "incorrect@email.faux"
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 302


def test_purchasePlaces(client):
    club = "Iron Temple"
    competition = "Fall Classic"
    places = '4'
    response = client.post('/purchasePlaces',
                           data={'club': club,
                                 'competition': competition,
                                 'places': places
                                 }
                           )
    assert response.status_code == 307
    response = client.post('/showSummary',
                           data={'club': club,
                                 'competition': competition,
                                 'places': places
                                 }
                           )
    assert b'Great-booking complete!' in response.data


def test_purchasePlaces_too_much(client):
    club = "Iron Temple"
    competition = "Fall Classic"
    places = '40'
    response = client.post('/purchasePlaces',
                           data={'club': club,
                                 'competition': competition,
                                 'places': places
                                 },
                           )
    assert response.status_code == 307
    response = client.post('/showSummary',
                           data={'club': club,
                                 'competition': competition,
                                 'places': places
                                 }
                           )
    assert b'You don&#39;t have enough points available' in response.data
