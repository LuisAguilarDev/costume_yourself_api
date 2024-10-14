from flask import Blueprint, request, jsonify

main = Blueprint('other_blueprint', __name__)


@main.route('/', methods=['GET'])
def login():
    print("entered")
    return 'soy otra ruta'
