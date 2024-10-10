"""
Este archivo contiene una aplicación básica de Flask.
"""

from flask import Flask

app = Flask(__name__)

"""
Este archivo contiene una aplicación básica de Flask.
"""

@app.route('/')
def home():
    """
    Esta función maneja la ruta raíz y devuelve un saludo.
    """
    return "¡Hola, Flask!"
