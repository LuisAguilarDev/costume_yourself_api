from flask import Flask
from flask_cors import CORS
# Routes
from src.routes import index_routes,other_routes

app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)
    CORS(app, resources={r"/last_step": {"origins": "https://costume-app.vercel.app"}})
    # Blueprints
    app.register_blueprint(index_routes.main, url_prefix='/')
    app.register_blueprint(other_routes.main, url_prefix='/other')

    return app
