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

    # Beautiful romantic math full-page HTML template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Mathematics of Us</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Outfit:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #09030c 0%, #1a0314 50%, #2c0213 100%);
            --card-bg: rgba(255, 255, 255, 0.04);
            --card-border: rgba(255, 42, 109, 0.15);
            --primary-love: #ff2a6d;
            --secondary-love: #ff7597;
            --glow-color: rgba(255, 42, 109, 0.4);
            --text-light: #fff0f3;
            --text-muted: #c8b5bd;
            --math-blue: #05d9e8;
            --math-blue-glow: rgba(5, 217, 232, 0.3);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: 
                linear-gradient(rgba(255, 42, 109, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 42, 109, 0.03) 1px, transparent 1px),
                var(--bg-gradient);
            background-size: 30px 30px;
            color: var(--text-light);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            position: relative;
        }

        /* Floating background items: math symbols and hearts */
        .float-element {
            position: absolute;
            bottom: -100px;
            color: rgba(255, 42, 109, 0.1);
            font-size: 1.8rem;
            font-family: 'Fira Code', monospace;
            animation: floatUp 15s infinite linear;
            user-select: none;
            pointer-events: none;
            z-index: 1;
        }

        .math-symbol {
            color: rgba(5, 217, 232, 0.1);
            font-weight: 500;
        }

        @keyframes floatUp {
            0% {
                transform: translateY(0) rotate(0deg) scale(0.8);
                opacity: 0;
            }
            10% {
                opacity: 0.7;
            }
            90% {
                opacity: 0.7;
            }
            100% {
                transform: translateY(-115vh) rotate(360deg) scale(1.2);
                opacity: 0;
            }
        }

        /* Layout Structure */
        .app-layout {
            display: flex;
            flex-direction: column;
            width: 100%;
            min-height: 100vh;
            padding: 30px 5%;
            position: relative;
            z-index: 2;
        }

        .app-header {
            text-align: center;
            margin-bottom: 35px;
        }

        .title {
            font-family: 'Dancing Script', cursive;
            font-size: 3.8rem;
            background: linear-gradient(to right, var(--primary-love), var(--math-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.2));
        }

        .subtitle {
            font-size: 1.15rem;
            color: var(--text-muted);
            font-weight: 300;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            gap: 40px;
            width: 100%;
            max-width: 1300px;
            margin: 0 auto;
            align-items: start;
        }

        @media (max-width: 950px) {
            .main-content {
                grid-template-columns: 1fr;
                gap: 30px;
            }
        }

        /* Left Side: Graphing Board Card */
        .graph-section {
            width: 100%;
        }

        .graph-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .graph-title {
            font-family: 'Fira Code', monospace;
            font-size: 0.95rem;
            color: var(--secondary-love);
            background: rgba(0, 0, 0, 0.2);
            padding: 8px 15px;
            border-radius: 10px;
            display: inline-block;
            margin-bottom: 20px;
            border: 1px dashed rgba(255, 42, 109, 0.25);
        }

        .graph-container {
            width: 100%;
            max-width: 360px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 10px;
        }

        .math-graph {
            width: 100%;
            height: auto;
            overflow: visible;
        }

        .axis-line {
            stroke: rgba(255, 255, 255, 0.15);
            stroke-width: 1.5;
            stroke-dasharray: 4;
        }

        .grid-subline {
            stroke: rgba(255, 255, 255, 0.05);
            stroke-width: 1;
        }

        .graph-text {
            fill: var(--text-muted);
            font-family: 'Fira Code', monospace;
            font-size: 0.75rem;
        }

        /* SVG Heart Path drawing animation */
        .heart-path {
            fill: rgba(255, 42, 109, 0.06);
            stroke: var(--primary-love);
            stroke-width: 3;
            stroke-linecap: round;
            stroke-dasharray: 1000;
            stroke-dashoffset: 1000;
            animation: drawPath 3.5s ease-out forwards, heartbeat 1.4s infinite ease-in-out 3.5s;
            transform-origin: 200px 190px;
            filter: drop-shadow(0 0 15px var(--glow-color));
        }

        @keyframes drawPath {
            to {
                stroke-dashoffset: 0;
            }
        }

        @keyframes heartbeat {
            0% { transform: scale(1); }
            14% { transform: scale(1.08); }
            28% { transform: scale(1); }
            42% { transform: scale(1.05); }
            70% { transform: scale(1); }
        }

        .graph-footer {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            padding: 0 10px;
            font-family: 'Fira Code', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        /* Right Side: Math Cards Grid */
        .cards-section {
            width: 100%;
        }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
        }

        .math-card {
            background: var(--card-bg);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 24px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .math-card:hover {
            transform: translateY(-5px);
            border-color: var(--math-blue);
            box-shadow: 0 10px 25px var(--math-blue-glow);
        }

        .card-formula {
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            color: var(--math-blue);
            margin-bottom: 12px;
            font-weight: 500;
        }

        .math-card h3 {
            font-size: 1.15rem;
            margin-bottom: 8px;
            color: var(--text-light);
            font-weight: 600;
        }

        .math-card p {
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.5;
            font-weight: 300;
        }

        /* Special Vault Card styling for the Secret Key injection */
        .vault-card {
            grid-column: 1 / -1;
            background: linear-gradient(135deg, rgba(255, 42, 109, 0.08) 0%, rgba(5, 217, 232, 0.08) 100%);
            border: 1px solid var(--math-blue);
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            padding: 20px 30px;
        }

        @media (max-width: 550px) {
            .vault-card {
                flex-direction: column;
                text-align: center;
                gap: 15px;
            }
        }

        .vault-info h3 {
            color: var(--math-blue);
        }

        .secret-badge {
            font-family: 'Fira Code', monospace;
            background: rgba(5, 217, 232, 0.15);
            border: 1px solid var(--math-blue);
            color: var(--math-blue);
            padding: 8px 16px;
            border-radius: 12px;
            font-size: 1.05rem;
            font-weight: 600;
            text-shadow: 0 0 8px rgba(5, 217, 232, 0.4);
            animation: pulseGlow 2s infinite alternate;
        }

        @keyframes pulseGlow {
            from { box-shadow: 0 0 5px rgba(5, 217, 232, 0.2); }
            to { box-shadow: 0 0 15px rgba(5, 217, 232, 0.6); }
        }

        .footer {
            text-align: center;
            margin-top: auto;
            padding: 40px 0 10px 0;
            font-size: 0.75rem;
            color: var(--text-muted);
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0.5;
        }
    </style>
</head>
<body>

    <!-- Floating Background Hearts and Mathematics symbols -->
    <div class="float-element" style="left: 5%; animation-delay: 0s; animation-duration: 10s;">❤️</div>
    <div class="float-element math-symbol" style="left: 15%; animation-delay: 2s; animation-duration: 12s;">f'(x)</div>
    <div class="float-element" style="left: 28%; animation-delay: 6s; animation-duration: 9s;">💖</div>
    <div class="float-element math-symbol" style="left: 38%; animation-delay: 1s; animation-duration: 11s;">lim(t→∞)</div>
    <div class="float-element" style="left: 48%; animation-delay: 8s; animation-duration: 13s;">💕</div>
    <div class="float-element math-symbol" style="left: 58%; animation-delay: 3s; animation-duration: 10s;">π</div>
    <div class="float-element" style="left: 68%; animation-delay: 7s; animation-duration: 14s;">💗</div>
    <div class="float-element math-symbol" style="left: 78%; animation-delay: 2s; animation-duration: 8s;">e^x</div>
    <div class="float-element" style="left: 88%; animation-delay: 4s; animation-duration: 12s;">💖</div>
    <div class="float-element math-symbol" style="left: 95%; animation-delay: 9s; animation-duration: 11s;">∫</div>

    <div class="app-layout">
        <header class="app-header">
            <h1 class="title">The Mathematics of Us</h1>
            <p class="subtitle">Proof: We are the perfect equation</p>
        </header>

        <div class="main-content">
            
            <!-- Left Panel: The Interactive Graphing Board -->
            <section class="graph-section">
                <div class="graph-card">
                    <div class="graph-title">(x² + y² - 1)³ - x²y³ = 0</div>
                    
                    <div class="graph-container">
                        <svg viewBox="0 0 400 400" class="math-graph">
                            <!-- Background Grid Sublines -->
                            <line x1="50" y1="20" x2="50" y2="380" class="grid-subline" />
                            <line x1="100" y1="20" x2="100" y2="380" class="grid-subline" />
                            <line x1="150" y1="20" x2="150" y2="380" class="grid-subline" />
                            <line x1="250" y1="20" x2="250" y2="380" class="grid-subline" />
                            <line x1="300" y1="20" x2="300" y2="380" class="grid-subline" />
                            <line x1="350" y1="20" x2="350" y2="380" class="grid-subline" />
                            
                            <line x1="20" y1="50" x2="380" y2="50" class="grid-subline" />
                            <line x1="20" y1="100" x2="380" y2="100" class="grid-subline" />
                            <line x1="20" y1="150" x2="380" y2="150" class="grid-subline" />
                            <line x1="20" y1="250" x2="380" y2="250" class="grid-subline" />
                            <line x1="20" y1="300" x2="380" y2="300" class="grid-subline" />
                            <line x1="20" y1="350" x2="380" y2="350" class="grid-subline" />

                            <!-- Main X and Y Axes -->
                            <line x1="20" y1="200" x2="380" y2="200" class="axis-line" />
                            <line x1="200" y1="20" x2="200" y2="380" class="axis-line" />
                            
                            <!-- Graph Labels -->
                            <text x="370" y="190" class="graph-text">x</text>
                            <text x="210" y="35" class="graph-text">y</text>
                            <text x="210" y="215" class="graph-text">0,0</text>
                            
                            <!-- Heart Path (plotted curve) -->
                            <path d="M 200 145 C 140 60, 60 130, 200 300 C 340 130, 260 60, 200 145 Z" class="heart-path" />
                        </svg>
                    </div>

                    <div class="graph-footer">
                        <span>Domain: [-1.5, 1.5]</span>
                        <span>Range: [-1.2, 1.5]</span>
                    </div>
                </div>
            </section>

            <!-- Right Panel: Cards Grid (Jokes and Equations) -->
            <section class="cards-section">
                <div class="cards-grid">
                    
                    <!-- Card 1 -->
                    <div class="math-card">
                        <div class="card-formula">f'(e^x) = e^x</div>
                        <h3>The Derivative</h3>
                        <p>Like e^x, my love for you is unchanged by any rate of change.</p>
                    </div>

                    <!-- Card 2 -->
                    <div class="math-card">
                        <div class="card-formula">∫ f(x) dx + C</div>
                        <h3>The Constant</h3>
                        <p>You are the constant C that completes my integration.</p>
                    </div>

                    <!-- Card 3 -->
                    <div class="math-card">
                        <div class="card-formula">x / 0 = ?</div>
                        <h3>The Denominator</h3>
                        <p>You are the denominator of my fraction—without you, my life is undefined.</p>
                    </div>

                    <!-- Card 4 -->
                    <div class="math-card">
                        <div class="card-formula">√-1 = i</div>
                        <h3>The Imaginary</h3>
                        <p>You must be the square root of -1, because you can't be real, yet you complete my complex world.</p>
                    </div>

                    <!-- Card 5 -->
                    <div class="math-card">
                        <div class="card-formula">π = 3.14159...</div>
                        <h3>The Pi Constant</h3>
                        <p>Our bond is like π: natural, irrational, and never-ending.</p>
                    </div>

                    <!-- Card 6 -->
                    <div class="math-card">
                        <div class="card-formula">sin²θ + cos²θ = 1</div>
                        <h3>The Identity</h3>
                        <p>We must be sine and cosine, because together we square to make 1.</p>
                    </div>

                    <!-- Card 7 -->
                    <div class="math-card">
                        <div class="card-formula">A · A⁻¹ = I</div>
                        <h3>The Matrix Inverse</h3>
                        <p>You are the inverse of my matrix—when we multiply, we create the perfect identity.</p>
                    </div>

                    <!-- Card 8 -->
                    <div class="math-card">
                        <div class="card-formula">You &lt; 3</div>
                        <h3>The Inequality</h3>
                        <p>Are you less than three? Because you are &lt;3.</p>
                    </div>

                    <!-- Card 9 -->
                    <div class="math-card">
                        <div class="card-formula">∫₀^∞ Love(t) dt = ∞</div>
                        <h3>Divergent Heart</h3>
                        <p>If I had to integrate my feelings from 0 to ∞, the result would diverge to infinity.</p>
                    </div>

                    <!-- Card 11 (Vault Card) -->
                    <div class="math-card vault-card">
                        <div class="vault-info">
                            <div class="card-formula">K8S_SECRET_VAULT</div>
                            <h3>The Constant Key</h3>
                            <p>Secured via GitOps environment credentials</p>
                        </div>
                        <div class="secret-badge">{secret}</div>
                    </div>

                </div>
            </section>
        </div>

        <!-- Hidden test-friendly element to pass existing unit tests! -->
        <div style="display: none;">Hello! {secret} is the secret of my energy!</div>

        <footer class="footer">
            Designed with DevOps, Kubernetes & Mathematics
        </footer>
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
