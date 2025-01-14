from src import init_app
from config import Settings
from waitress import serve

app = init_app(Settings)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)