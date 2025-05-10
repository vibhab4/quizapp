import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code in [200, 400]

def test_login(client):
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert 'api_key' in response.get_json()

def test_invalid_login(client):
    response = client.post('/api/login', json={
        "username": "nonexistentuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.get_json()['error'] == "Invalid username or password"

def test_duplicate_register(client):
    client.post('/api/register', json={
        "username": "dupeuser",
        "password": "pass123"
    })
    response = client.post('/api/register', json={
        "username": "dupeuser",
        "password": "pass123"
    })
    assert response.status_code == 400  # or 409 depending on your app logic
