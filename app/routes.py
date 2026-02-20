"""
Routes pour l'API de prédiction
"""
from flask import Blueprint, request, jsonify, render_template
from app.services import get_prediction_service
import logging
import traceback

logger = logging.getLogger(__name__)

predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint POST pour effectuer une prédiction
    
    Requête JSON:
    {
        "Opérateur": "...",
        "Quartier": "...",
        "Type réseau": "...",
        "Download (Mbps)": ...,
        "Upload (Mbps)": ...,
        "Latence (ms)": ...,
        "Jitter (ms)": ...,
        "Loss (%)": ...
    }
    
    Réponse JSON:
    {
        "prediction": "Bonne|Moyenne|Mauvaise",
        "predicted_class": 0|1|2,
        "confidence": 0-1,
        "probabilities": {
            "Bonne": ...,
            "Moyenne": ...,
            "Mauvaise": ...
        }
    }
    """
    try:
        # Vérifier que la requête contient du JSON
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type doit être application/json',
                'message': 'Veuillez envoyer une requête JSON'
            }), 400
        
        # Récupérer les données
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Données vides',
                'message': 'Le corps de la requête ne peut pas être vide'
            }), 400
        
        # Effectuer la prédiction
        service = get_prediction_service()
        result = service.predict(data)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
    
    except ValueError as e:
        logger.error(f"Erreur de validation: {e}")
        return jsonify({
            'error': 'Erreur de validation',
            'message': str(e),
            'details': traceback.format_exc()
        }), 400
    
    except RuntimeError as e:
        logger.error(f"Erreur runtime: {e}")
        return jsonify({
            'error': 'Erreur du serveur',
            'message': str(e),
            'details': traceback.format_exc()
        }), 500
    
    except Exception as e:
        logger.error(f"Erreur non gérée: {e}")
        return jsonify({
            'error': 'Erreur interne du serveur',
            'message': str(e),
            'details': traceback.format_exc()
        }), 500


@predict_bp.route('/predict/schema', methods=['GET'])
def predict_schema():
    """
    Endpoint GET pour obtenir le schéma de l'API
    """
    try:
        service = get_prediction_service()
        
        schema = {
            'numeric_fields': {
                col: 'float' for col in service.numeric_columns
            },
            'categorical_fields': {
                col: 'string' for col in service.categorical_columns
            },
            'output_classes': list(service.target_mapping.values()),
            'example_request': {
                "Opérateur": "Orange",
                "Quartier": "Centre",
                "Type réseau": "5G",
                "Download (Mbps)": 100,
                "Upload (Mbps)": 50,
                "Latence (ms)": 10,
                "Jitter (ms)": 2,
                "Loss (%)": 0.1
            }
        }
        
        return jsonify({
            'success': True,
            'schema': schema
        }), 200
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du schéma: {e}")
        return jsonify({
            'error': 'Erreur interne du serveur',
            'message': str(e)
        }), 500


@predict_bp.route('/api/test', methods=['GET'])
def api_test():
    """
    Endpoint de test pour vérifier que l'API fonctionne
    """
    return jsonify({
        'status': 'ok',
        'message': 'API Test endpoint working'
    }), 200
