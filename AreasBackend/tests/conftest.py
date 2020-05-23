import pytest
import http.client
from areas_backend.app import create_app
from .constants import PRIVATE_KEY
from areas_backend import token_validation
from faker import Faker
fake = Faker()


@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    application.db.create_all()

    return application


@pytest.fixture
def area_fixture(client):
    '''
    Generate three areas in the system.
    '''

    area_ids = []
    for _ in range(3):
        area = {
            'areacode': fake.text(240),
            'area': fake.text(240),
            'zonecode': fake.text(240),
        }
        header = token_validation.generate_token_header(fake.name(),
                                                        PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.post('/api/me/areas/', data=area,
                               headers=headers)
        assert http.client.CREATED == response.status_code
        result = response.json
        area_ids.append(result['id'])

    yield area_ids

    # Clean up all areas
    response = client.get('/api/areas/')
    areas = response.json
    for area in areas:
        area_id = area['id']
        url = f'/admin/areas/{area_id}/'
        response = client.delete(url)
        assert http.client.NO_CONTENT == response.status_code
