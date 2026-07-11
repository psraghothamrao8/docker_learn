import os  # Import the built-in operating system library to inspect or modify environment variables.

# Import our Flask application instance (the 'app' variable) from the 'app.py' file.
# This lets us access the app's routing and configuration directly in our tests.
from app import app

# Pytest (our testing tool) automatically searches for and executes any functions whose names start with "test_".
def test_home_route():
    # Create a test client using Flask's built-in testing support.
    # The test client acts like a virtual browser, allowing us to send mock requests
    # to our app without needing to spin up a real web server process.
    client = app.test_client()
    
    # Simulate a web browser sending an HTTP GET request to the homepage ('/') route.
    response = client.get('/')
    
    # Verify that our application responds with a 200 HTTP status code.
    # Status code 200 means 'OK'—the server successfully handled the request.
    assert response.status_code == 200
    
    # Verify that the response data contains our expected text.
    # 1. The 'assert' keyword tests if the condition is True. If False, the test fails.
    # 2. 'response.data' contains the raw HTML sent back by the server.
    # 3. The 'b' prefix before the string (e.g. b"...") creates a "bytes" object.
    #    Since 'response.data' is raw bytes, we must search for a bytes string.
    # 4. We check for "Hello! pavvi is the secret of my energy!" because 'pavvi' is 
    #    the SECRET_KEY environment variable configured during our testing phase.
    assert b"Hello! pavvi is the secret of my energy!" in response.data