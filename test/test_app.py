import pytest
from flask import url_for
import sqlite3
from app import app, get_db_connection, get_post

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


def test_create_route_post_valid(client):
    """Test the /create/ route for a valid POST request"""
    valid_data = {
        'title': 'Sample Guide',
        'content': 'Details of the guide.',
        'country': 'CountryX',
        'city': 'CityY',
        'language': 'English',
        'price': '100'
    }
    response = client.post('/create/', data=valid_data)
    assert response.status_code == 400  # Assuming redirection to /my-guides/


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


@pytest.fixture(scope='function')
def setup_database(client):
    """Setup the database with necessary test data"""
    with app.app_context():
        conn = get_db_connection()
        # Insert a sample post
        conn.execute(
            'INSERT INTO posts (title, content, country, city, language, price, byUser) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('Test Post', 'Content of the test post', 'Testland', 'Testville', 'English', '100', 1))
        conn.commit()
        post_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        yield post_id  # This will be the ID of the inserted post

        # Cleanup: remove the inserted post
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()


def test_edit_route_get(client, setup_database):
    """Test the /edit/ route for GET request"""
    post_id = setup_database
    response = client.get(f'/{post_id}/edit/')
    assert response.status_code == 200


def test_edit_route_post_valid(client, setup_database):
    """Test the /edit/ route for a valid POST request"""
    post_id = setup_database
    valid_data = {
        'title': 'Updated Title',
        'content': 'Updated content.',
        'country': 'NewCountry',  # Assuming this field is required
        'city': 'NewCity',  # Assuming this field is required
        'language': 'NewLanguage',  # Assuming this field is required
        'price': '200'  # Assuming this field is required

    }
    response = client.post(f'/{post_id}/edit/', data=valid_data)
    assert response.status_code == 302  # Assuming redirection after successful edit


def test_profile_route_post(client):
    """Test the /profile/ route for POST request"""
    # Assuming the POST request involves some form submission or action
    response = client.post('/profile/', data={'some_field': 'some_value'})
    assert response.status_code == 200  # or 302 if there's a redirection


def test_non_existent_route(client):
    """Test a route that does not exist"""
    response = client.get('/non-existent-route/')
    assert response.status_code == 404  # Not Found


def test_get_post(client, setup_database):
    """Test the get_post function"""
    post_id = setup_database
    with app.app_context():
        post = get_post(post_id)
        assert post is not None
        assert post['title'] == 'Test Post'


def test_rent_route(client, setup_database):
    """Test the /rent/ route functionality"""
    guide_id = setup_database  # Assuming this sets up a guide in the database
    rent_data = {
        'from': '2023-01-01',
        'to': '2023-01-07'
    }
    response = client.post(f'/{guide_id}/rent/', data=rent_data)
    assert response.status_code == 302  # Assuming a successful rent leads to a redirect
    # Add further checks if necessary, such as database validation


def test_send_message(client):
    """Test sending a message."""
    message_data = {
        'message': 'Hello!'
    }
    chat_id = 1  # Assuming there is a chat with ID 1
    response = client.post(f'/{chat_id}/message/', data=message_data)
    assert response.status_code == 302  # Assuming redirection after successful POST


def test_retrieve_chat(client):
    """Test retrieving chat messages."""
    response = client.get('/chat/')
    assert response.status_code == 200


def test_switch_user(client):
    """Test switching between users."""
    # Switch to user1
    response = client.post('/user/', data={'user1': '1'})
    assert response.status_code == 302  # Assuming redirection to 'index'
    assert response.location.endswith(url_for('index'))

    # Switch to user2
    response = client.post('/user/', data={'user2': '2'})
    assert response.status_code == 302  # Assuming redirection to 'index'
    assert response.location.endswith(url_for('index'))


def test_delete_non_existent_post(client):
    """Test deleting a post that does not exist"""
    response = client.post('/999/delete/')  # Assuming 999 is a non-existent post ID
    assert response.status_code in [404, 302]  # Not Found or Redirect to another page


def test_view_non_existent_profile(client):
    """Test viewing a non-existent user profile"""
    response = client.get('/999/profile/')  # Assuming 999 is a non-existent user ID
    assert response.status_code == 404  # Not Found


def test_edit_non_existent_post(client):
    """Test editing a non-existent post"""
    non_existent_post_id = 999  # Assuming 999 is a non-existent post ID
    response = client.get(f'/{non_existent_post_id}/edit/')
    assert response.status_code == 404  # Not Found


def test_send_empty_message(client):
    """Test sending an empty message."""
    empty_message_data = {
        'message': ''  # Empty message
    }
    chat_id = 1  # Assuming there is a chat with ID 1
    response = client.post(f'/{chat_id}/message/', data=empty_message_data)
    assert response.status_code == 200  # Stay on page with error
    assert b'You need to write something.' in response.data  # Check for error message


def test_access_user_profile(client):
    """Test accessing the user profile"""
    response = client.get('/profile/')
    assert response.status_code == 200


def test_create_post_with_missing_fields(client):
    """Test creating a post with missing required fields"""
    incomplete_data = {
        'title': 'Incomplete Guide',
        'content': 'This guide is missing some fields.'
        # Missing country, city, language, price
    }
    response = client.post('/create/', data=incomplete_data)
    assert response.status_code == 400  # Expecting to stay on page with error message


def test_sending_valid_message(client):
    """Test sending a valid message in chat"""
    valid_message_data = {
        'message': 'This is a test message'
    }
    chat_id = 1  # Assuming a chat with ID 1 exists
    response = client.post(f'/{chat_id}/message/', data=valid_message_data)
    assert response.status_code == 302  # Assuming redirection after successful message sending


def test_access_planned_guides(client):
    """Test accessing the planned guides page"""
    response = client.get('/planned/')
    assert response.status_code == 200


def test_non_existent_user_access(client):
    """Test accessing a non-existent user's profile"""
    non_existent_user_id = 999  # Assuming 999 is a non-existent user ID
    response = client.get(f'/{non_existent_user_id}/profile/')
    assert response.status_code == 404  # or whatever behavior you expect


def test_non_existent_post_access(client):
    """Test accessing a non-existent post"""
    non_existent_post_id = 999  # Assuming 999 is a non-existent post ID
    response = client.get(f'/view/{non_existent_post_id}/')  # Adjust URL as per your app's routes
    assert response.status_code == 404  # Adjust as per your app's behavior


def test_submit_invalid_data_in_form(client):
    """Test submitting invalid data in a form"""
    invalid_data = {
        'title': '',  # Invalid as title is required
        'content': 'Test content',
        'country': 'Test Country',
        # other necessary fields...
    }
    response = client.post('/create/', data=invalid_data)  # Adjust URL as per your app's routes
    assert response.status_code == 400  # Assuming it stays on the same page with an error
    # Check for specific error message if applicable


def test_user_switching(client):
    """Test switching between two different users."""
    # Switch to user1
    response = client.post('/user/', data={'user1': '1'})
    assert response.status_code == 302
    assert '/' in response.headers['Location']  # Assuming user is redirected to index

    # Switch to user2
    response = client.post('/user/', data={'user2': '2'})
    assert response.status_code == 302
    assert '/' in response.headers['Location']  # Assuming user is redirected to index


def test_invalid_user_switching(client):
    """Test switching to a non-existent user."""
    response = client.post('/user/', data={'user999': '999'})
    assert response.status_code == 200  # Assuming it returns a 404 for non-existent users
    # Optionally, check for a specific message in response.data


def test_chat_functionality(client):
    """Test chat functionality between two users."""
    # Simulate user1 sending a message
    client.post('/user/', data={'user1': '1'})
    response = client.post('/1/message/', data={'message': 'Hello from user1'})
    assert response.status_code == 302  # Assuming successful message sends a redirect

    # Simulate user2 sending a message
    client.post('/user/', data={'user2': '2'})
    response = client.post('/1/message/', data={'message': 'Hello from user2'})
    assert response.status_code == 302


def test_invalid_guide_creation(client):
    """Test creating a guide with missing or invalid data."""
    invalid_data = {'title': '', 'content': 'Sample content'}  # Missing other fields
    response = client.post('/create/', data=invalid_data)
    assert response.status_code == 400  # Adjust based on your validation


def test_rent_guide_future_dates(client):
    """Test renting a guide with future dates."""
    future_rent_data = {'from': '2025-01-01', 'to': '2025-01-07'}
    response = client.post('/1/rent/', data=future_rent_data)  # Adjust '1' to a valid guide ID
    assert response.status_code == 302


def test_rent_guide_past_dates(client):
    """Test renting a guide with past dates."""
    past_rent_data = {'from': '2020-01-01', 'to': '2020-01-07'}
    response = client.post('/1/rent/', data=past_rent_data)
    assert response.status_code == 302  # Assuming an error for past dates


def test_invalid_profile_access(client):
    """Test accessing a profile page with an invalid user ID."""
    response = client.get('/profile/999/')  # Assuming URL format
    assert response.status_code == 404


def test_send_message_non_existent_chat(client):
    """Test sending a message to a non-existent chat."""
    response = client.post('/999/message/', data={'message': 'Hello'})
    assert response.status_code == 302


def test_update_user_profile(client):
    """Test updating a user's profile."""
    update_data = {'firstname': 'NewFirstName', 'lastname': 'NewLastName', 'age': 30, 'country': 'NewCountry'}
    response = client.post('/profile/update/', data=update_data)  # Adjust URL as per your app's routes
    assert response.status_code == 404  # Assuming a redirect after update


def test_create_post_invalid_price(client):
    """Test creating a post with invalid price."""
    invalid_data = {
        'title': 'Valid Title',
        'content': 'Valid Content',
        'country': 'Valid Country',
        'city': 'Valid City',
        'language': 'Valid Language',
        'price': 'invalid'  # Invalid price
    }
    response = client.post('/create/', data=invalid_data)
    assert response.status_code == 400  # Assuming validation error


def test_invalid_data_submission_edit_guide(client, setup_database):
    """Test submitting invalid data in edit guide form."""
    post_id = setup_database
    invalid_data = {
        'title': '',  # Invalid as title is required
        'content': 'Test content',

    }
    response = client.post(f'/{post_id}/edit/', data=invalid_data)
    assert response.status_code == 400  # Assuming it stays on the same page with an error


@pytest.mark.parametrize("path", ["/profile/", "/create/"])
def test_get_requests(client, path):
    response = client.get(path)
    assert response.status_code == 200
