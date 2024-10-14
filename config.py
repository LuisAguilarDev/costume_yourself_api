from decouple import config


class Settings:
    CLOUD_NAME_CLOUDINARY:str = config('CLOUD_NAME_CLOUDINARY')
    API_KEY_CLOUDINARY:str = config('API_KEY_CLOUDINARY')
    API_SECRET_CLOUDINARY:str = config('API_SECRET_CLOUDINARY')
    CLOUDINARY_URL:str = config('CLOUDINARY_URL')
class DevelopmentConfig(Settings):
    DEBUG = True

configurations = {
    'development': DevelopmentConfig
}
