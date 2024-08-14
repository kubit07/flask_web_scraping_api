from datetime import timedelta
import os
from decouple import config


BASE_DIR=os.path.dirname(os.path.realpath(__file__))
BASE_DIR_DATA_SCRAPING_WINDOWS = (r"C:\Users\dvesa\data_scraping\data_scraping")
#BASE_DIR_DATA_SCRAPING_LINUX = (r"C:\Users\dvesa\data_scraping\data_scraping")

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    # Token for 90 days 
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=90)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=90)
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')

class DevConfig(Config):
    DEBUG=config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'db.sqlite3')

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI="sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True

class ProdConfig(Config):
    pass


config_dict={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}