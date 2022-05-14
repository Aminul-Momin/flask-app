import os
#==============================================================================
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'f837176ba8e206da1a580bd66654bcf9'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    
    # IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"
    # SESSION_COOKIE_SECURE = True


class ProdConfig(Config):
    DB_NAME = "prod-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "12345"


class DevConfig(Config):
    
    DEBUG = True

    DB_NAME = "dev-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "12345"

    # IMAGE_UPLOADS = "/home/username/projects/my_app/app/static/images/uploads"
    # SESSION_COOKIE_SECURE = False


class TestConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False