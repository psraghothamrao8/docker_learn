import os  # Import the operating system library (can be used to inspect or set environment variables)

# Import our Flask application instance 'app' from the 'app.py' file
from app import app

# Pytest automatically discovers and runs functions whose names start with "test_"
def test_home_route():
    # Create a test client using Flask's built-in testing support.
    # This allows us to simulate HTTP requests to our application without actually running a web server.
    client = app.test_client()
    
    # Simulate an HTTP GET request to the homepage ('/') route
    response = client.get('/')
    
    # Verify that the server responded with an HTTP status code 200 (which means 'OK' / success)
    assert response.status_code == 200
    
    # Verify that the response content contains our expected secret text.
    # The 'b' prefix in b"..." defines a bytes literal, since response.data is returned as bytes.
    # We expect 'pavvi' to be printed here because that's our configured secret in the test environment.
    assert b"Hello! pavvi is the secret of my energy!" in response.data