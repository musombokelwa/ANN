
"""
Client Python pour tester l'API de prédiction de qualité réseau
Peut être utilisé comme module ou script autonome
"""

import requests
import json
import sys
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class PredictionResult:
    """Résultat de prédiction"""
    prediction: str
    predicted_class: int
    confidence: float
    probabilities: Dict[str, float]
    input_features: Dict[str, Any]
    
    def __str__(self):
        return f"""
Résultat de Prédiction
Prédiction: {self.prediction}
Confiance: {self.confidence * 100:.2f}%
Classe: {self.predicted_class}

Probabilités:
{json.dumps(self.probabilities, indent=2)}

Entrées:
{json.dumps(self.input_features, indent=2)}
"""


class NetworkQualityAPIClient:
    """Client pour l'API de prédiction de qualité réseau"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialiser le client
        
        Args:
            base_url: URL de base de l'API (sans trailing slash)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def health_check(self) -> bool:
        """
        Vérifier que l'API est disponible
        
        Returns:
            True si l'API répond, False sinon
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Erreur lors du health check: {e}")
            return False
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Récupérer le schéma de l'API
        
        Returns:
            Dictionnaire contenant le schéma
        """
        try:
            response = self.session.get(f"{self.base_url}/predict/schema", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('schema', {})
        except Exception as e:
            print(f"Erreur lors de la récupération du schéma: {e}")
            return {}
    
    def predict(self, data: Dict[str, Any]) -> Optional[PredictionResult]:
        """
        Effectuer une prédiction
        
        Args:
            data: Dictionnaire avec les données d'entrée
            
        Returns:
            PredictionResult si succès, None sinon
        """
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            json_response = response.json()
            
            if not json_response.get('success'):
                print(f"Erreur API: {json_response.get('error')}")
                return None
            
            result = json_response.get('result', {})
            
            return PredictionResult(
                prediction=result.get('prediction'),
                predicted_class=result.get('predicted_class'),
                confidence=result.get('confidence'),
                probabilities=result.get('probabilities', {}),
                input_features=result.get('input_features', {})
            )
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête: {e}")
            return None
        except Exception as e:
            print(f"Erreur lors de la prédiction: {e}")
            return None


def test_excellent_connection(client: NetworkQualityAPIClient):
    """Tester une excellente connexion"""
    print("\n" + "="*50)
    print("TEST: Excellente Connexion")
    print("="*50)
    
    data = {
        "Opérateur": "Orange",
        "Quartier": "Centre",
        "Type réseau": "5G",
        "Download (Mbps)": 200,
        "Upload (Mbps)": 100,
        "Latence (ms)": 5,
        "Jitter (ms)": 1,
        "Loss (%)": 0
    }
    
    result = client.predict(data)
    if result:
        print(result)
        assert result.prediction == "Bonne", f"Attendu 'Bonne' mais got '{result.prediction}'"
        print("✅ Test réussi!")


def test_medium_connection(client: NetworkQualityAPIClient):
    """Tester une connexion moyenne"""
    print("\n" + "="*50)
    print("🟡 TEST: Connexion Moyenne")
    print("="*50)
    
    data = {
        "Opérateur": "Maroc Telecom",
        "Quartier": "Tahrir",
        "Type réseau": "4G",
        "Download (Mbps)": 50,
        "Upload (Mbps)": 25,
        "Latence (ms)": 30,
        "Jitter (ms)": 5,
        "Loss (%)": 1
    }
    
    result = client.predict(data)
    if result:
        print(result)
        assert result.prediction == "Moyenne", f"Attendu 'Moyenne' mais got '{result.prediction}'"
        print(" Test réussi!")


def test_poor_connection(client: NetworkQualityAPIClient):
    """Tester une mauvaise connexion"""
    print("\n" + "="*50)
    print("TEST: Mauvaise Connexion")
    print("="*50)
    
    data = {
        "Opérateur": "Vodafone",
        "Quartier": "Souissi",
        "Type réseau": "3G",
        "Download (Mbps)": 10,
        "Upload (Mbps)": 5,
        "Latence (ms)": 100,
        "Jitter (ms)": 20,
        "Loss (%)": 5
    }
    
    result = client.predict(data)
    if result:
        print(result)
        assert result.prediction == "Mauvaise", f"Attendu 'Mauvaise' mais got '{result.prediction}'"
        print("Test réussi!")


def interactive_mode(client: NetworkQualityAPIClient):
    """Mode interactif pour tester l'API"""
    print("\n" + "="*50)
    print(" Mode Interactif")
    print("="*50)
    
    print("\nEntrez les données de la connexion réseau:")
    
    data = {}
    fields = {
        "Opérateur": "str",
        "Quartier": "str",
        "Type réseau": "str",
        "Download (Mbps)": "float",
        "Upload (Mbps)": "float",
        "Latence (ms)": "float",
        "Jitter (ms)": "float",
        "Loss (%)": "float"
    }
    
    for field, field_type in fields.items():
        while True:
            try:
                value = input(f"  {field}: ")
                if field_type == "float":
                    data[field] = float(value)
                else:
                    data[field] = value
                break
            except ValueError:
                print(f" Entrée invalide. Attendu {field_type}")
    
    result = client.predict(data)
    if result:
        print(result)


def main():
    """Fonction principale"""
    print("="*50)
    print("Network Quality Prediction - API Client")
    print("="*50)
    
    # Créer le client
    client = NetworkQualityAPIClient()
    
    # Vérifier la connexion à l'API
    print("\n Vérification de la connexion à l'API...")
    if not client.health_check():
        print(" Impossible de se connecter à l'API!")
        print(f"   Assurez-vous que l'API fonctionne sur {client.base_url}")
        sys.exit(1)
    
    print("Connexion établie!")
    
    # Afficher le schéma
    print("\n Récupération du schéma...")
    schema = client.get_schema()
    if schema:
        print("Schéma reçu!")
        print(json.dumps(schema, indent=2))
    
    # Menu
    print("\n" + "="*50)
    print("Menu Options:")
    print("1. Tester excellente connexion")
    print("2. Tester connexion moyenne")
    print("3. Tester mauvaise connexion")
    print("4. Mode interactif")
    print("5. Quitter")
    print("="*50)
    
    while True:
        choice = input("\nChoisissez une option (1-5): ").strip()
        
        if choice == "1":
            test_excellent_connection(client)
        elif choice == "2":
            test_medium_connection(client)
        elif choice == "3":
            test_poor_connection(client)
        elif choice == "4":
            interactive_mode(client)
        elif choice == "5":
            print("\n À bientôt!")
            sys.exit(0)
        else:
            print("Option invalide. Essayez encore.")


if __name__ == "__main__":
    main()
