import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    # os.environ.get reads the secret injected by Docker
    secret = os.environ.get('SECRET_KEY', 'no-key-found')
    
    return f"Hello! {secret} is the secret of my energy!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)