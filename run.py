from src import init_app
from config import Settings
from flask_cors import CORS
app = init_app(Settings)
