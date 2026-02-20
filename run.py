#!/usr/bin/env python3
"""
Application Flask pour la prédiction de qualité réseau
Point d'entrée principal de l'application
"""

import os
import sys
import logging
from app import create_app
from flask import render_template

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Créer l'application Flask
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# Handlers d'erreurs personnalisés
@app.errorhandler(404)
def not_found_error(error):
    """Gérer les routes non trouvées"""
    return {
        'error': 'Not Found',
        'message': 'La ressource demandée n\'existe pas',
        'status': 404
    }, 404

@app.errorhandler(500)
def internal_error(error):
    """Gérer les erreurs internes du serveur"""
    logger.error(f"Erreur interne du serveur: {error}")
    return {
        'error': 'Internal Server Error',
        'message': 'Une erreur interne s\'est produite',
        'status': 500
    }, 500

@app.errorhandler(405)
def method_not_allowed(error):
    """Gérer les méthodes non autorisées"""
    return {
        'error': 'Method Not Allowed',
        'message': 'La méthode HTTP n\'est pas autorisée pour cette route',
        'status': 405
    }, 405

if __name__ == '__main__':
    # Déterminer le mode (production ou développement)
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Déterminer l'adresse et le port
    host = os.environ.get('FLASK_HOST', '0.0.0.0')  # Écouter sur toutes les interfaces
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    logger.info(f"Starting Network Quality Prediction API")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"Server will be accessible at: http://{host}:{port}")
    
    # Démarrer le serveur
    try:
        app.run(
            host=host,
            port=port,
            debug=debug_mode,
            use_reloader=debug_mode,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)
