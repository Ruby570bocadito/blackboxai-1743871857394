from flask import Flask, render_template
from config import Config
from database import db, migrate
# Import models after db is initialized
from database.models import Campaign, Target, Event, Response

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
import logging
from logging.handlers import RotatingFileHandler

# Set up file logging with absolute path
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/flask.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
file_handler = RotatingFileHandler(log_path, maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('SocialPhantom startup')

# Initialize database
db.init_app(app)
migrate.init_app(app, db)

# Create tables in development mode
if app.config['DEBUG']:
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Failed to create database tables: {e}")

# Import blueprints
from scenario_generator import scenario_bp
from web_cloner import cloner_bp
from email_sender import email_bp
from payload_generator import payload_bp
from campaign_manager import campaign_bp
from dashboard import dashboard_bp

# Register blueprints
app.register_blueprint(scenario_bp)
app.register_blueprint(cloner_bp)
app.register_blueprint(email_bp)
app.register_blueprint(payload_bp)
app.register_blueprint(campaign_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)