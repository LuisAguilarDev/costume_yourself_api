from flask import Blueprint

main = Blueprint('index_blueprint', __name__)


@main.route('/')
def index():
    return "¡Hola, Flask 2!"
