import pytest
from app import app, get_db_connection


# Configure the app for testing
app.config['TESTING'] = True

@pytest.fixture(scope='function')
def client():
    """Setup test client for Flask app"""
    with app.test_client() as client:
        with app.app_context():
            # Setup: Create the necessary tables
            conn = get_db_connection()
            with app.open_resource('schema.sql', mode='r') as f:
                conn.cursor().executescript(f.read())
            conn.commit()

        yield client

        with app.app_context():
            # Teardown: Drop the tables after each test
            conn = get_db_connection()
            conn.execute('DROP TABLE IF EXISTS posts')
            conn.execute('DROP TABLE IF EXISTS user')
            conn.commit()


def test_index(client):
    """Test the index route"""
    response = client.get('/')
    assert response.status_code == 200


def test_user_route_get(client):
    """Test the /user/ route for GET request"""
    response = client.get('/user/')
    assert response.status_code == 200


def test_user_route_post_user1(client):
    """Test the /user/ route for POST request with user1"""
    response = client.post('/user/', data={'user1': '1'})
    assert response.status_code == 302
    assert response.location.endswith('/')


def test_user_route_post_user2(client):
    """Test the /user/ route for POST request with user2"""
    response = client.post('/user/', data={'user2': '2'})
    assert response.status_code == 302
    assert response.location.endswith('/')


def test_chat_route(client):
    """Test the /chat/ route"""
    response = client.get('/chat/')
    assert response.status_code == 200


def test_my_guides_route(client):
    """Test the /my-guides/ route"""
    response = client.get('/my-guides/')
    assert response.status_code == 200


def test_profile_route_get(client):
    """Test the /profile/ route for GET request"""
    response = client.get('/profile/')
    assert response.status_code == 200


def test_create_route_get(client):
    """Test the /create/ route for GET request"""
    response = client.get('/create/')
    assert response.status_code == 200

# ... add more tests for other routes ...
