import os
# Mock a fake secret just for the test environment before loading the app
# os.environ['SECRET_KEY'] = 'pavvi'

from app import app

def test_home_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello! pavvi is the secret of my energy" in response.data