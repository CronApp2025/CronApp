
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': '0.0.0.0',  # Using 0.0.0.0 instead of localhost
    'user': 'root',
    'password': '',
    'database': 'cronapp_2025',
    'port': 3306  # MySQL default port
}

# Mail configuration
MAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD')
}

# App configuration
APP_CONFIG = {
    'SECRET_KEY': os.getenv('SESSION_SECRET', 'your-secret-key'),
    'SECURITY_PASSWORD_SALT': 'password-reset-salt'
}

DATABASE_URL = os.getenv('DATABASE_URL')

JWT_SECRET_KEY = os.getenv('SECRET_KEY', APP_CONFIG['SECRET_KEY'])

EXPIRE_TOKEN_TIME = {
    "ACCESS_TOKEN_MINUTES": 60,
    "REFRESH_TOKEN_DAYS": 30
}

TOKEN_BLACKLIST_ENABLED = True
