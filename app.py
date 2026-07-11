import os  # Import the built-in operating system library to access environment variables
from flask import Flask  # Import the Flask class from the flask framework to create our web app

# Initialize the Flask application.
# __name__ is a special Python variable that helps Flask locate resources like templates and static files.
app = Flask(__name__)

# Define the route for the root URL ('/').
# When a user visits the website home page, this 'home' function will be executed.
@app.route('/')
def home():
    # Retrieve the value of the environment variable 'SECRET_KEY'.
    # If 'SECRET_KEY' is not defined (e.g. not injected by Docker/system), default to 'no-key-found'.
    secret = os.environ.get('SECRET_KEY', 'no-key-found')

    # Return a text greeting to the user's browser, displaying the secret.
    return f"Hello! {secret} is the secret of my energy!"

# The main entry point check.
# This block runs only if we execute this script directly (e.g., 'python app.py').
# It will NOT run if this script is imported by another Python file (like in our tests).
if __name__ == '__main__':
    # Start the Flask development web server.
    # host='0.0.0.0' configures Flask to listen on all available network interfaces.
    # port=5000 configures Flask to listen on port number 5000.
    app.run(host='0.0.0.0', port=5000)