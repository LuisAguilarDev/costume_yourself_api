from config import configurations  # Importa el diccionario correcto
from flask_cors import CORS
from src import init_app

# Accede a la configuración de desarrollo
Configuration = configurations['development']

# Inicializa la aplicación con la configuración seleccionada
app = init_app(Configuration)
CORS(app) 

if __name__ == '__main__':
    app.run()
