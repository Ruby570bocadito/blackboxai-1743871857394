#!/usr/bin/env python3
import os
from app import app, db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize app
app.config.from_object('config.Config')

# Create necessary directories
os.makedirs('campaigns', exist_ok=True)
os.makedirs('clones', exist_ok=True)
os.makedirs('payloads', exist_ok=True)
os.makedirs('logs', exist_ok=True)

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        
    # Run the application
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False') == 'True'
    )