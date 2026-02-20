"""
Application Flask pour la prédiction de qualité réseau
"""
from flask import Flask
from flask_cors import CORS


def create_app(config_name='development'):
    """Factory function pour créer l'application Flask"""
    import os
    from config import get_config
    
    # Déterminer les chemins des dossiers
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    
    # Créer l'app avec les bons chemins
    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir)
    
    # Charger la configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Activer CORS pour les requêtes cross-origin
    CORS(app)
    
    # Enregistrer les blueprints
    from app.routes import predict_bp
    app.register_blueprint(predict_bp)
    
    # Route de santé
    @app.route('/health', methods=['GET'])
    def health():
        """Endpoint de santé pour vérifier que l'API fonctionne"""
        return {
            'status': 'healthy',
            'message': 'API Network Quality Prediction is running'
        }, 200
    
    # Route racine - Interface Web
    @app.route('/', methods=['GET'])
    def index():
        """Page d'accueil avec interface web"""
        from flask import render_template
        return render_template('index.html')
    
    return app
