# Configuration pour le déploiement Flask

import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Limits
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    JSON_MAXSIZE = 16 * 1024 * 1024
    
    # Sessions
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False
    ENV = 'development'

class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False
    ENV = 'production'

class TestingConfig(Config):
    """Configuration de test"""
    DEBUG = True
    TESTING = True
    ENV = 'testing'

# Sélectionner la configuration selon l'environnement
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config(env=None):
    """Récupérer la configuration"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
