from flask import Flask

# Routes
from src.routes import index_routes,other_routes

app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(index_routes.main, url_prefix='/')
    app.register_blueprint(other_routes.main, url_prefix='/other')

    return app
