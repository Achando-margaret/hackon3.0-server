import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    # PostgreSQL with psycopg v3
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg://username:password@localhost/study_bloom'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True if os.environ.get('DEBUG') == '1' else False
