import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_changed_in_production'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates' # Not explicitly used for SPA, but good practice
    VIDEOS_FOLDER = 'videos'
    DOCS_FOLDER = 'docs'

    # Hugging Face API
    HF_API_TOKEN = os.environ.get('HF_API_TOKEN')
    HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"

    # Optional: Stripe & Intercom (placeholders)
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    INTERCOM_ACCESS_TOKEN = os.environ.get('INTERCOM_ACCESS_TOKEN')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    # In production, ensure SECRET_KEY is set via environment variable
    # HF_API_TOKEN should also be set in production environment

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'testing'

def get_config():
    """Returns the appropriate configuration based on FLASK_ENV."""
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    return DevelopmentConfig