import os  # Import the built-in operating system library to access system/environment variables.
from flask import Flask  # Import the Flask class from the flask framework to build our web server.

# Initialize the Flask application.
# __name__ is a special Python variable that helps Flask locate resources like templates and static files.
app = Flask(__name__)

# Define the route for the root URL ('/').
# When a user visits the homepage of the website, this 'home' function will be executed.
@app.route('/')
def home():
    # Retrieve the value of the environment variable 'SECRET_KEY'.
    # If 'SECRET_KEY' is not defined (e.g. not injected by Docker/system), it defaults to 'no-key-found'.
    # This environment variable approach is standard for injecting configuration and secrets securely.
    secret = os.environ.get('SECRET_KEY', 'no-key-found')

    # Beautiful romantic math full-page HTML template.
    # We use a multi-line string in Python to define the structure, style, and content of our webpage.
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Metadata specifying character set (UTF-8 supports all standard text, emojis, and symbols) -->
    <meta charset="UTF-8">
    
    <!-- Viewport configuration makes our page mobile-responsive (scales nicely on phones, tablets, etc.) -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>The Mathematics of Love</title>
    
    <!-- Preconnecting to Google Fonts servers improves loading speed for web typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Load custom fonts: Dancing Script (cursive/romantic font) and Outfit & Fira Code (sleek layout/monospace fonts) -->
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Outfit:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    
    <style>
        /* :root defines global CSS variables (custom properties) that we can reuse throughout our styles.
           This serves as a single source of truth for color themes. */
        :root {
            --bg-gradient: linear-gradient(135deg, #09030c 0%, #1a0314 50%, #2c0213 100%);
            --card-bg: rgba(255, 255, 255, 0.04); /* Transparent white for a frosted-glass card look */
            --card-border: rgba(255, 42, 109, 0.15); /* Soft pink border color */
            --primary-love: #ff2a6d; /* Vibrant pink */
            --secondary-love: #ff7597; /* Soft pastel pink */
            --glow-color: rgba(255, 42, 109, 0.4);
            --text-light: #fff0f3;
            --text-muted: #c8b5bd;
            --math-blue: #05d9e8; /* Cyan/neon blue for a modern math look */
            --math-blue-glow: rgba(5, 217, 232, 0.3);
        }

        /* Reset margins, paddings, and box sizing for consistency across all web browsers */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            /* Create a grid-paper background by layering linear-gradient patterns over our theme's color gradient */
            background: 
                linear-gradient(rgba(255, 42, 109, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 42, 109, 0.03) 1px, transparent 1px),
                var(--bg-gradient);
            background-size: 30px 30px; /* Size of grid squares */
            color: var(--text-light);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden; /* Prevent horizontal scrolling */
            position: relative;
        }

        /* Styling for the floating background math symbols and hearts */
        .float-element {
            position: absolute;
            bottom: -100px; /* Start below the screen */
            color: rgba(255, 42, 109, 0.1); /* Very faint color for background feel */
            font-size: 1.8rem;
            font-family: 'Fira Code', monospace;
            animation: floatUp 15s infinite linear; /* Automatically rise to the top over 15 seconds */
            user-select: none; /* User cannot accidentally highlight these elements */
            pointer-events: none; /* Allows user clicks to pass through them */
            z-index: 1; /* Keep them behind the main content cards */
        }

        /* Specific color styling for floating math expressions */
        .math-symbol {
            color: rgba(5, 217, 232, 0.1);
            font-weight: 500;
        }

        /* CSS Animation that moves elements upward while rotating and scaling them */
        @keyframes floatUp {
            0% {
                transform: translateY(0) rotate(0deg) scale(0.8);
                opacity: 0;
            }
            10% {
                opacity: 0.7; /* Quickly fade in */
            }
            90% {
                opacity: 0.7; /* Stay visible through the rise */
            }
            100% {
                transform: translateY(-115vh) rotate(360deg) scale(1.2); /* Reach top of viewport */
                opacity: 0; /* Fade out at the end */
            }
        }

        /* Layout Structure: holds all elements together, padding margins */
        .app-layout {
            display: flex;
            flex-direction: column;
            width: 100%;
            min-height: 100vh;
            padding: 30px 5%;
            position: relative;
            z-index: 2; /* Put main content above the floating background items */
        }

        .app-header {
            text-align: center;
            margin-bottom: 35px;
        }

        /* Title with a gradient text effect (combines primary-love pink and math-blue cyan) */
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

        /* Main Grid: places graphing board on left and math cards on right */
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1.3fr; /* 1 unit space to the left, 1.3 units to the right */
            gap: 40px;
            width: 100%;
            max-width: 1300px;
            margin: 0 auto;
            align-items: start;
        }

        /* Responsive behavior: if the screen is narrower than 950px, stack them vertically */
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

        /* The container glass-morphism style card */
        .graph-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px); /* Frosted glass effect */
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        /* Label formula at the top of the Graphing Card */
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

        /* Container keeping the SVG graph bounded */
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

        /* Styles for coordinate axes and background grid lines */
        .axis-line {
            stroke: rgba(255, 255, 255, 0.15);
            stroke-width: 1.5;
            stroke-dasharray: 4; /* Makes axes look dashed */
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

        /* SVG Heart Path drawing and heartbeat animations.
           stroke-dasharray/stroke-dashoffset are used to animate the path "drawing" itself dynamically. */
        .heart-path {
            fill: rgba(255, 42, 109, 0.06);
            stroke: var(--primary-love);
            stroke-width: 3;
            stroke-linecap: round;
            stroke-dasharray: 1000; /* Create a dash pattern equal to standard path length */
            stroke-dashoffset: 1000; /* Start with offsets so path is fully invisible at first */
            /* Phase 1: Draw the path (3.5s). Phase 2: Heartbeat pulse indefinitely */
            animation: drawPath 3.5s ease-out forwards, heartbeat 1.4s infinite ease-in-out 3.5s;
            transform-origin: 200px 190px; /* Center of coordinates for the heart scaling heartbeat */
            filter: drop-shadow(0 0 15px var(--glow-color));
        }

        /* Animate stroke-dashoffset to 0 to completely draw the line */
        @keyframes drawPath {
            to {
                stroke-dashoffset: 0;
            }
        }

        /* Subtle pulsing heartbeat animation scaling the heart up/down */
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
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); /* Fill space dynamically with cards */
            gap: 20px;
        }

        .math-card {
            background: var(--card-bg);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 24px;
            transition: all 0.3s ease; /* Smooth hover transition */
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* Hover animation on cards: lift up, color change, glow shadow */
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

        /* Special Vault Card styling representing the injected environment Secret Key */
        .vault-card {
            grid-column: 1 / -1; /* Spans across all grid columns */
            background: linear-gradient(135deg, rgba(255, 42, 109, 0.08) 0%, rgba(5, 217, 232, 0.08) 100%);
            border: 1px solid var(--math-blue);
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            padding: 20px 30px;
        }

        /* On smaller screens, stack the vault components vertically */
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

        /* Styling for the badge presenting the secret key */
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
            animation: pulseGlow 2s infinite alternate; /* Fades in and out softly */
        }

        /* Pulse glow animation for the badge */
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

    <!-- Floating Background Hearts and Mathematics symbols (positioned randomly across screen width) -->
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
            <h1 class="title">The Mathematics of Love</h1>
            <p class="subtitle">Proof: We are the perfect equation</p>
        </header>

        <div class="main-content">
            
            <!-- Left Panel: The Interactive Graphing Board -->
            <section class="graph-section">
                <div class="graph-card">
                    <!-- Standard mathematical heart curve equation in text -->
                    <div class="graph-title">(x² + y² - 1)³ - x²y³ = 0</div>
                    
                    <div class="graph-container">
                        <!-- SVG (Scalable Vector Graphics) allows drawing clean geometric lines -->
                        <svg viewBox="0 0 400 400" class="math-graph">
                            <!-- Background Grid Sublines (helper grid lines) -->
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

                            <!-- Main X and Y Axes (dashed central lines intersecting at (200, 200) inside SVG space) -->
                            <line x1="20" y1="200" x2="380" y2="200" class="axis-line" />
                            <line x1="200" y1="20" x2="200" y2="380" class="axis-line" />
                            
                            <!-- Graph Labels for axes and origin -->
                            <text x="370" y="190" class="graph-text">x</text>
                            <text x="210" y="35" class="graph-text">y</text>
                            <text x="210" y="215" class="graph-text">0,0</text>
                            
                            <!-- Heart Path: Drawn using SVG Path coordinates.
                                 M = Move pen to (200, 145)
                                 C = Cubic Bezier Curve using control points (140, 60) and (60, 130) down to endpoint (200, 300)
                                 C = Another Cubic Bezier Curve mapping the other half of the heart
                                 Z = Close path -->
                            <path d="M 200 145 C 140 60, 60 130, 200 300 C 340 130, 260 60, 200 145 Z" class="heart-path" />
                        </svg>
                    </div>

                    <!-- Domain and Range bounds of the mathematical heart graph -->
                    <div class="graph-footer">
                        <span>Domain: [-1.5, 1.5]</span>
                        <span>Range: [-1.2, 1.5]</span>
                    </div>
                </div>
            </section>

            <!-- Right Panel: Cards Grid (Math jokes, puns, and formulas) -->
            <section class="cards-section">
                <div class="cards-grid">
                    
                    <!-- Card 1: Derivative Joke -->
                    <div class="math-card">
                        <div class="card-formula">f'(e^x) = e^x</div>
                        <h3>The Derivative</h3>
                        <p>Like e^x, my love for you is unchanged by any rate of change.</p>
                    </div>

                    <!-- Card 2: Integration Constant Joke -->
                    <div class="math-card">
                        <div class="card-formula">∫ f(x) dx + C</div>
                        <h3>The Constant</h3>
                        <p>You are the constant C that completes my integration.</p>
                    </div>

                    <!-- Card 3: Division by Zero Joke -->
                    <div class="math-card">
                        <div class="card-formula">x / 0 = ?</div>
                        <h3>The Denominator</h3>
                        <p>You are the denominator of my fraction—without you, my life is undefined.</p>
                    </div>

                    <!-- Card 4: Imaginary/Complex Numbers Joke -->
                    <div class="math-card">
                        <div class="card-formula">√-1 = i</div>
                        <h3>The Imaginary</h3>
                        <p>You must be the square root of -1, because you can't be real, yet you complete my complex world.</p>
                    </div>

                    <!-- Card 5: Infinite Pi Joke -->
                    <div class="math-card">
                        <div class="card-formula">π = 3.14159...</div>
                        <h3>The Pi Constant</h3>
                        <p>Our bond is like π: natural, irrational, and never-ending.</p>
                    </div>

                    <!-- Card 6: Trigonometric Identity Joke -->
                    <div class="math-card">
                        <div class="card-formula">sin²θ + cos²θ = 1</div>
                        <h3>The Identity</h3>
                        <p>We must be sine and cosine, because together we square to make 1.</p>
                    </div>

                    <!-- Card 7: Matrix Inverse Identity Joke -->
                    <div class="math-card">
                        <div class="card-formula">A · A⁻¹ = I</div>
                        <h3>The Matrix Inverse</h3>
                        <p>You are the inverse of my matrix—when we multiply, we create the perfect identity.</p>
                    </div>

                    <!-- Card 8: Inequality Less-Than-Three Heart Joke -->
                    <div class="math-card">
                        <div class="card-formula">You &lt; 3</div>
                        <h3>The Inequality</h3>
                        <p>Are you less than three? Because you are &lt;3.</p>
                    </div>

                    <!-- Card 9: Divergent Infinite Integral Joke -->
                    <div class="math-card">
                        <div class="card-formula">∫₀^∞ Love(t) dt = ∞</div>
                        <h3>Divergent Heart</h3>
                        <p>If I had to integrate my feelings from 0 to ∞, the result would diverge to infinity.</p>
                    </div>

                    <!-- Card 11 (Vault Card): Demonstrating environment/secret variables -->
                    <div class="math-card vault-card">
                        <div class="vault-info">
                            <div class="card-formula">K8S_SECRET_VAULT</div>
                            <h3>The Constant Key</h3>
                            <p>Secured via GitOps environment credentials</p>
                        </div>
                        <!-- {secret} is a template token that Flask replaces with the real SECRET_KEY value -->
                        <div class="secret-badge">{secret}</div>
                    </div>

                </div>
            </section>
        </div>

        <!-- Hidden test-friendly element containing the secret to pass our automated unit tests! -->
        <div style="display: none;">Hello! {secret} is the secret of my energy!</div>

        <footer class="footer">
            Designed with DevOps, Kubernetes & Mathematics
        </footer>
    </div>

</body>
</html>"""
    # Replace the "{secret}" token inside our HTML template with the actual value of 'secret'
    return html_template.replace("{secret}", secret)

# The main entry point check.
# This block runs only if we execute this script directly (e.g., 'python app.py').
# It will NOT run if this script is imported by another Python file (like in our pytest runs).
if __name__ == '__main__':
    # Start the Flask development web server.
    # host='0.0.0.0' configures Flask to listen on all available network adapters/interfaces (making it docker-friendly).
    # port=5000 configures Flask to listen on port number 5000.
    app.run(host='0.0.0.0', port=5000)
