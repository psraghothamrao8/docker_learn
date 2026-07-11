import os  # Import the operating system library to manipulate environment variables and directory paths.
from app import app  # Import our Flask application instance to generate static content from it.

# GitHub Pages serves static files (HTML, CSS, JS) but does not run active Python/Flask backend servers.
# To deploy there, we pre-render our dynamic website into a flat, static HTML file.

# 1. Set the SECRET_KEY environment variable. 
# This ensures that when the page is generated, 'GitHub Pages Live' is baked into the template's secret badge.
os.environ['SECRET_KEY'] = 'GitHub Pages Live'

# 2. Use Flask's test client to simulate a user visiting our homepage.
client = app.test_client()
response = client.get('/')

# 3. Ensure the output directory 'dist' (distribution) exists.
# exist_ok=True prevents Python from throwing an error if the directory already exists.
os.makedirs('dist', exist_ok=True)

# 4. Open and write the generated HTML bytes to a file at 'dist/index.html'.
# 'wb' stands for "Write Binary" because the test client response.data is returned in bytes.
# Using 'with' is a Python best practice (context manager) that guarantees the file is safely closed after writing.
with open('dist/index.html', 'wb') as f:
    f.write(response.data)

print("Successfully exported static site to dist/index.html")
