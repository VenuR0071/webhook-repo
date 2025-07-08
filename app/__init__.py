# webhook-repo/app/__init__.py
from flask import Flask, render_template
import os
from .extensions import init_db_connection
from .webhook.routes import webhook_bp

def create_app():
    app = Flask(__name__, template_folder='../templates') # Set template_folder explicitly

    # Load configurations from environment variables
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['DB_NAME'] = os.getenv('DB_NAME')
    app.config['COLLECTION_NAME'] = os.getenv('COLLECTION_NAME')

    # Initialize MongoDB connection
    init_db_connection(app)

    # Register blueprints
    app.register_blueprint(webhook_bp)

    # UI serving endpoint (from the root '/')
    @app.route('/')
    def index():
        return render_template('index.html')

    return app