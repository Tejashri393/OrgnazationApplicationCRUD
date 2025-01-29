
import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
SECRET_KEY = os.getenv('SECRET_KEY', 'tejashri')
