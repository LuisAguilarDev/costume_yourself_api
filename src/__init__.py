import logging
from flask import Flask
from flask_cors import CORS
# Routes
from src.routes import index_routes,other_routes

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

def init_app(config):
    # Configuration
    app.config.from_object(config)
    # Blueprints
    app.register_blueprint(index_routes.main, url_prefix='/')
    app.register_blueprint(other_routes.main, url_prefix='/other')

    return app
