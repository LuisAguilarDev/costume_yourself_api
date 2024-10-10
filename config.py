from decouple import config


class Settings:
    SECRET_KEY = config('SECRET_KEY')


class DevelopmentConfig(Settings):
    DEBUG = True


# Renombrar el diccionario para evitar conflicto
configurations = {
    'development': DevelopmentConfig
}
