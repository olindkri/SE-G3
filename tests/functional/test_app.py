import sqlite3
import pytest
from flask import Flask
from app import app, get_db_connection, get_post, get_user


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        yield client


def test_get_db_connection():
    conn = get_db_connection()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_get_post(client):
    # Replace this with a valid post_id from your database
    post_id = 1
    post = get_post(post_id)
    assert post is not None


def test_get_user(client):
    # Replace this with a valid user_id from your database
    user_id = 1
    user = get_user(user_id)
    assert user is not None


def test_user_route(client):
    response = client.post('/user/', data={'user1': '1'})
    assert response.status_code == 302  # Redirect
    assert response.location.endswith('/')


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200


def test_chat_route(client):
    response = client.get('/chat/')
    assert response.status_code == 200


def test_guides_route(client):
    response = client.get('/my-guides/')
    assert response.status_code == 200


def test_profile_route(client):
    response = client.get('/profile/')
    assert response.status_code == 200


def test_create_route(client):
    response = client.get('/create/')
    assert response.status_code == 200


def test_edit_route(client):
    response = client.get('/1/edit/')  # Replace '1' with a valid post ID
    assert response.status_code == 200


def test_view_route(client):
    response = client.get('/1/view/')  # Replace '1' with a valid post ID
    assert response.status_code == 200


def test_message_route(client):
    response = client.get('/1/message/')  # Replace '1' with a valid chat ID
    assert response.status_code == 200


def test_delete_route(client):
    response = client.post('/1/delete/')  # Replace '1' with a valid post ID
    assert response.status_code == 302  # Redirect
    assert response.location.endswith('/')

# Add more tests as needed for your specific use cases
