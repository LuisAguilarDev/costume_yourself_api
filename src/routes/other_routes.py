from flask import Blueprint, request, jsonify

main = Blueprint('other_blueprint', __name__)


@main.route('/')
def login():
    print("entered")
    return 'soy otra ruta'
