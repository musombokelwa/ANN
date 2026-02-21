"""
Tests unitaires pour l'API de prédiction
"""

import pytest
import json
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import app


@pytest.fixture
def client():
    """Créer un client de test"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests pour l'endpoint /health"""
    
    def test_health_check(self, client):
        """Tester que le serveur est en bonne santé"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestSchemaEndpoint:
    """Tests pour l'endpoint /predict/schema"""
    
    def test_get_schema(self, client):
        """Tester la récupération du schéma"""
        response = client.get('/predict/schema')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'schema' in data
        assert 'numeric_fields' in data['schema']
        assert 'categorical_fields' in data['schema']


class TestPredictEndpoint:
    """Tests pour l'endpoint /predict"""
    
    @pytest.fixture
    def valid_input(self):
        """Données valides pour la prédiction"""
        return {
            "Opérateur": "Orange",
            "Quartier": "Centre",
            "Type réseau": "5G",
            "Download (Mbps)": 100,
            "Upload (Mbps)": 50,
            "Latence (ms)": 10,
            "Jitter (ms)": 2,
            "Loss (%)": 0.1
        }
    
    def test_valid_prediction(self, client, valid_input):
        """Tester une prédiction valide"""
        response = client.post(
            '/predict',
            data=json.dumps(valid_input),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'result' in data
        assert 'prediction' in data['result']
        assert 'confidence' in data['result']
        assert 'probabilities' in data['result']
    
    def test_empty_request(self, client):
        """Tester une requête vide"""
        response = client.post(
            '/predict',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_missing_fields(self, client):
        """Tester avec des champs manquants"""
        incomplete_data = {
            "Opérateur": "Orange",
            "Download (Mbps)": 100
        }
        response = client.post(
            '/predict',
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_invalid_content_type(self, client):
        """Tester avec un Content-Type invalide"""
        response = client.post(
            '/predict',
            data='invalid',
            content_type='text/plain'
        )
        assert response.status_code == 400
    
    def test_prediction_output_contains_quality_class(self, client):
        """Tester que la prédiction contient une classe de qualité valide"""
        valid_data = {
            "Opérateur": "Orange",
            "Quartier": "Centre",
            "Type réseau": "5G",
            "Download (Mbps)": 100,
            "Upload (Mbps)": 50,
            "Latence (ms)": 10,
            "Jitter (ms)": 2,
            "Loss (%)": 0.1
        }
        response = client.post(
            '/predict',
            data=json.dumps(valid_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        prediction = data['result']['prediction']
        assert prediction in ["Bonne", "Moyenne", "Mauvaise"]


class TestNotFoundEndpoint:
    """Tests pour les erreurs 404"""
    
    def test_not_found(self, client):
        """Tester une route inexistante"""
        response = client.get('/inexistent')
        assert response.status_code == 404


class TestMethodNotAllowed:
    """Tests pour les erreurs 405"""
    
    def test_get_on_post_endpoint(self, client):
        """Tester une requête GET sur un endpoint POST"""
        response = client.get('/predict')
        assert response.status_code == 405


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
