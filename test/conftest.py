import pytest
from app import server



@pytest.fixture
def app():
    app = server.app
    app.config.update(({'TESTING': True}))
    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
        
        

@pytest.fixture
def mock_clubs(mocker):
    data = [
        {
            "name": "Club 1",
            "email": "club1@test.com",
            "points": "10"
        },
        {
            "name": "Club 2",
            "email": "club2@test.com",
            "points": "20"
        }
    ]
    mocker.patch.object(server, 'clubs', data)   