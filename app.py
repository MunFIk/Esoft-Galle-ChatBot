from flask import Flask
from flask_session import Session
from routes import chatbot_bp
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key
app.config['JSON_AS_ASCII'] = False  # Allow non-ASCII characters in JSON responses
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem to store session data
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # Session lifetime in seconds (30 minutes)

# Initialize Flask-Session
Session(app)

# Register blueprint
app.register_blueprint(chatbot_bp)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return "The requested page was not found.", 404

@app.errorhandler(500)
def internal_error(error):
    return "An internal error occurred.", 500

if __name__ == '__main__':
    # Run the app
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,       # Default port
        debug=True,      # Enable debug mode
        threaded=True    # Enable threading for better performance
    )
