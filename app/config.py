"""Flask configuration variables."""
from os import environ, path

import secrets

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = secrets.token_urlsafe(16)
    FLASK_APP = 'demo'

    # Database
    # SQLALCHEMY_DATABASE_URI = 'db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db/sample_demo_db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@172.18.0.3:3306/sample_demo_db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-User settings
    USER_APP_NAME = "Demo Sample"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True  # Enable email authentication
    USER_ENABLE_USERNAME = False  # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
    JWT_TOKEN_EXPIRE = 300
    USER_ROLE_NORMAL = "user"  # 0
    USER_ROLE_ADMIN = "admin"  # 1
    USER_ROLE_SUPER_ADMIN = "sa"  # 2
    JWT_ALGORITHMS = "HS256"
