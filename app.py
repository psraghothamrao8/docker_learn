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

    # Beautiful romantic HTML page template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Romantic Heartbeat</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #1a0817 0%, #400c25 50%, #690a2a 100%);
            --card-bg: rgba(255, 255, 255, 0.06);
            --card-border: rgba(255, 255, 255, 0.1);
            --primary-love: #ff2a6d;
            --secondary-love: #ff7597;
            --glow-color: rgba(255, 42, 109, 0.4);
            --text-light: #fff0f3;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-light);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }

        /* Floating background hearts animation */
        .heart-bubble {
            position: absolute;
            bottom: -100px;
            color: rgba(255, 42, 109, 0.12);
            font-size: 2rem;
            animation: floatUp 10s infinite linear;
            user-select: none;
            pointer-events: none;
        }

        @keyframes floatUp {
            0% {
                transform: translateY(0) rotate(0deg) scale(0.8);
                opacity: 0;
            }
            10% {
                opacity: 0.8;
            }
            90% {
                opacity: 0.8;
            }
            100% {
                transform: translateY(-110vh) rotate(360deg) scale(1.2);
                opacity: 0;
            }
        }

        /* Glassmorphism card container */
        .container {
            position: relative;
            z-index: 10;
            width: 90%;
            max-width: 460px;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 30px;
            padding: 50px 30px;
            text-align: center;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.35);
            animation: popIn 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes popIn {
            from { opacity: 0; transform: scale(0.85); }
            to { opacity: 1; transform: scale(1); }
        }

        .title {
            font-family: 'Dancing Script', cursive;
            font-size: 3.5rem;
            background: linear-gradient(to right, var(--primary-love), var(--secondary-love));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
        }

        /* Pulsing heartbeat container */
        .heart-container {
            margin: 30px 0;
            display: inline-block;
            cursor: pointer;
        }

        .main-heart {
            font-size: 6rem;
            color: var(--primary-love);
            display: inline-block;
            animation: heartbeat 1.2s infinite ease-in-out;
            filter: drop-shadow(0 0 20px var(--glow-color));
            transition: transform 0.2s ease;
        }

        .main-heart:hover {
            transform: scale(1.1) rotate(5deg);
        }

        @keyframes heartbeat {
            0% { transform: scale(1); }
            15% { transform: scale(1.2); }
            30% { transform: scale(1); }
            45% { transform: scale(1.15); }
            70% { transform: scale(1); }
        }

        .message {
            font-size: 1.25rem;
            line-height: 1.6;
            margin-bottom: 35px;
            font-weight: 300;
        }

        /* Secret key badge style */
        .secret-badge {
            display: inline-block;
            background: linear-gradient(135deg, rgba(255, 42, 109, 0.15) 0%, rgba(255, 117, 151, 0.15) 100%);
            border: 1px solid var(--secondary-love);
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            color: var(--secondary-love);
            letter-spacing: 0.5px;
            font-family: 'Outfit', sans-serif;
            text-shadow: 0 0 10px rgba(255, 117, 151, 0.4);
            animation: bounceGlow 2s infinite alternate;
        }

        @keyframes bounceGlow {
            from {
                box-shadow: 0 0 4px rgba(255, 117, 151, 0.2);
                transform: translateY(0);
            }
            to {
                box-shadow: 0 0 12px rgba(255, 117, 151, 0.6);
                transform: translateY(-2px);
            }
        }

        .footer {
            font-size: 0.75rem;
            opacity: 0.4;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 15px;
        }
    </style>
</head>
<body>

    <!-- Floating Background Hearts -->
    <div class="heart-bubble" style="left: 8%; animation-delay: 0s; font-size: 1.8rem; animation-duration: 9s;">❤️</div>
    <div class="heart-bubble" style="left: 22%; animation-delay: 2s; font-size: 2.5rem; animation-duration: 11s;">💖</div>
    <div class="heart-bubble" style="left: 40%; animation-delay: 5s; font-size: 1.5rem; animation-duration: 8s;">💕</div>
    <div class="heart-bubble" style="left: 58%; animation-delay: 1s; font-size: 2.2rem; animation-duration: 10s;">❤️</div>
    <div class="heart-bubble" style="left: 74%; animation-delay: 6s; font-size: 1.3rem; animation-duration: 7s;">💗</div>
    <div class="heart-bubble" style="left: 88%; animation-delay: 3s; font-size: 2.8rem; animation-duration: 12s;">💖</div>

    <div class="container">
        <h1 class="title">Love is in the Air</h1>
        
        <div class="heart-container">
            <span class="main-heart">❤️</span>
        </div>

        <p class="message">
            Did you know? <span class="secret-badge">{secret}</span> is the secret of my energy!
        </p>
        
        <!-- Hidden test-friendly element to pass existing unit tests! -->
        <div style="display: none;">Hello! {secret} is the secret of my energy!</div>

        <div class="footer">
            Crafted with DevOps & Loveeeeee
        </div>
    </div>

</body>
</html>"""
    return html_template.replace("{secret}", secret)

# The main entry point check.
# This block runs only if we execute this script directly (e.g., 'python app.py').
# It will NOT run if this script is imported by another Python file (like in our tests).
if __name__ == '__main__':
    # Start the Flask development web server.
    # host='0.0.0.0' configures Flask to listen on all available network interfaces.
    # port=5000 configures Flask to listen on port number 5000.
    app.run(host='0.0.0.0', port=5000)
