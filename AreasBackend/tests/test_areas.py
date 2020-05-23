'''
Test the Areas operations


Use the area_fixture to have data to retrieve, it generates three areas
'''
from unittest.mock import ANY
import http.client
from freezegun import freeze_time
from .constants import PRIVATE_KEY
from areas_backend import token_validation
from faker import Faker
fake = Faker()


@freeze_time('2019-05-07 13:47:34')
def test_create_me_area(client):
    new_area = {
        'username': fake.name(),
        'areacode': fake.text(240),
        'area': fake.text(240),
        'zonecode': fake.text(240),
    }
    header = token_validation.generate_token_header(fake.name(),
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/areas/', data=new_area,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'username': ANY,
        'areacode': new_area['areacode'],
        'area': new_area['area'],
        'zonecode': new_area['zonecode'],
        'timestamp': '2019-05-07T13:47:34',
    }
    assert result == expected


def test_create_me_unauthorized(client):
    new_area = {
        'username': fake.name(),
        'areacode': fake.text(240),
        'area': fake.text(240),
        'zonecode': fake.text(240),
    }
    response = client.post('/api/me/areas/', data=new_area)
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_me_areas(client, area_fixture):
    username = fake.name()
    areacode = fake.text(240)
    area = fake.text(240)
    zonecode = fake.text(240)

    # Create a new area
    new_area = {
        'areacode': areacode,
        'area': area,
        'zonecode': zonecode,
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/areas/', data=new_area,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    # Get the areas of the user
    response = client.get('/api/me/areas/', headers=headers)
    results = response.json

    assert http.client.OK == response.status_code
    assert len(results) == 1
    result = results[0]
    expected_result = {
        'id': ANY,
        'username': username,
        'areacode': areacode,
        'area': area,
        'zonecode': zonecode,
        'timestamp': ANY,
    }
    assert result == expected_result


def test_list_me_unauthorized(client):
    response = client.get('/api/me/areas/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_areas(client, area_fixture):
    response = client.get('/api/areas/')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the ids are increasing
    previous_id = -1
    for area in result:
        expected = {
            'areacode': ANY,
            'area': ANY,
            'zonecode': ANY,
            'username': ANY,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == area
        assert area['id'] > previous_id
        previous_id = area['id']


def test_list_areas_search(client, area_fixture):
    username = fake.name()
    new_area = {
        'username': username,
        'areacode': 'A tale about a Platypus',
        'area': 'A tale about a Platypus',
        'zonecode': 'A tale about a Platypus'
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/areas/', data=new_area,
                           headers=headers)
    assert http.client.CREATED == response.status_code

    response = client.get('/api/areas/?search=platypus')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the returned values contain "platypus"
    for area in result:
        expected = {
            'areacode': ANY,
            'area': ANY,
            'zonecode': ANY,
            'username': username,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == area
        assert 'platypus' in area['areacode'].lower()
        assert 'platypus' in area['area'].lower()
        assert 'platypus' in area['zonecode'].lower()


def test_get_area(client, area_fixture):
    area_id = area_fixture[0]
    response = client.get(f'/api/areas/{area_id}/')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'areacode' in result
    assert 'area' in result
    assert 'zonecode' in result
    assert 'username' in result
    assert 'timestamp' in result
    assert 'id' in result


def test_get_non_existing_area(client, area_fixture):
    area_id = 123456
    response = client.get(f'/api/areas/{area_id}/')

    assert http.client.NOT_FOUND == response.status_code
