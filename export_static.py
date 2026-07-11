import os
from app import app

# Set the environment variable that app.py expects for the secret key
os.environ['SECRET_KEY'] = 'GitHub Pages Live'

# Create a test client to simulate browser requests
client = app.test_client()
response = client.get('/')

# Ensure the output directory 'dist' exists
os.makedirs('dist', exist_ok=True)

# Write the rendered HTML content to dist/index.html
with open('dist/index.html', 'wb') as f:
    f.write(response.data)

print("Successfully exported static site to dist/index.html")
