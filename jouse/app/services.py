"""
Service de prédiction pour le modèle de qualité réseau
"""
import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class PredictionService:
    """Service pour charger le modèle et effectuer les prédictions"""
    
    _instance = None
    
    def __new__(cls):
        """Pattern Singleton pour charger le modèle une seule fois"""
        if cls._instance is None:
            cls._instance = super(PredictionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialiser le service et charger le modèle"""
        if self._initialized:
            return
        
        self.model = None
        self.scaler = None
        self.le_operateur = None
        self.le_quartier = None
        self.le_type_reseau = None
        self.le_qualite = None
        
        # Colonnes utilisées pour l'entraînement
        self.numeric_columns = [
            "Download (Mbps)",
            "Upload (Mbps)",
            "Latence (ms)",
            "Jitter (ms)",
            "Loss (%)"
        ]
        
        self.categorical_columns = [
            "Opérateur",
            "Quartier",
            "Type réseau"
        ]
        
        self.target_mapping = {
            0: "Bonne",
            1: "Moyenne",
            2: "Mauvaise"
        }
        
        # Charger le modèle et le scaler
        self._load_model_and_scaler()
        self._initialized = True
    
    def _load_model_and_scaler(self):
        """Charger le modèle et le scaler depuis les fichiers"""
        model_path = os.path.join(
            os.path.dirname(__file__),
            '../model/modele_non_entraine.pkl'
        )
        scaler_path = os.path.join(
            os.path.dirname(__file__),
            '../model/scaler.pkl'
        )
        
        try:
            # Vérifier que les fichiers existent
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Modèle non trouvé: {model_path}")
            if not os.path.exists(scaler_path):
                raise FileNotFoundError(f"Scaler non trouvé: {scaler_path}")
            
            # Charger le modèle et le scaler
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            
            logger.info("Modèle et scaler chargés avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            raise
    
    def preprocess_input(self, data: Dict[str, Any]) -> Tuple[np.ndarray, Dict]:
        """
        Prétraiter les données d'entrée selon le même processus qu'en entraînement
        
        Args:
            data: Dictionnaire avec les données d'entrée
            
        Returns:
            Tuple (données prétraitées, métadonnées)
        """
        try:
            # Créer un DataFrame à partir des données
            df = pd.DataFrame([data])
            
            # Valider que toutes les colonnes requises sont présentes
            required_columns = self.numeric_columns + self.categorical_columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                error_msg = f"Colonnes manquantes: {', '.join(missing_columns)}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Sélectionner uniquement les colonnes requises
            df = df[required_columns]
            
            # Encoder les colonnes catégoriques (conversion en nombres)
            # Utiliser un encoding simple basé sur la première occurrence
            for cat_col in self.categorical_columns:
                # Pour chaque catégorie, créer un hash numérique stable
                cat_value = str(df[cat_col].iloc[0])
                # Utiliser hash() pour obtenir un nombre entier stable
                encoded_value = abs(hash(cat_value)) % 1000
                df[cat_col] = encoded_value
            
            # Convertir les colonnes catégoriques en float
            df[self.categorical_columns] = df[self.categorical_columns].astype('float32')
            
            # Normaliser les colonnes numériques avec le scaler
            df[self.numeric_columns] = self.scaler.transform(df[self.numeric_columns])
            
            # Convertir en array numpy avec le bon ordre de colonnes
            # L'ordre doit être: catégories puis numériques
            ordered_columns = self.categorical_columns + self.numeric_columns
            X = df[ordered_columns].values.astype('float32')
            
            metadata = {
                'original_data': data,
                'preprocessed_shape': X.shape,
                'numeric_columns': self.numeric_columns,
                'categorical_columns': self.categorical_columns,
                'column_order': ordered_columns
            }
            
            return X, metadata
        
        except Exception as e:
            logger.error(f"Erreur lors du prétraitement: {e}")
            raise
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Effectuer une prédiction
        
        Args:
            data: Dictionnaire avec les données d'entrée
            
        Returns:
            Dictionnaire avec la prédiction
        """
        try:
            # Prétraiter les données
            X, metadata = self.preprocess_input(data)
            
            # Effectuer la prédiction
            if self.model is None:
                raise RuntimeError("Modèle non chargé")
            
            # Obtenir les prédictions et probabilités
            prediction = self.model.predict(X)  # Classe prédite
            probabilities = self.model.predict_proba(X)  # Probabilités pour chaque classe
            
            # Obtenir la classe prédite et la confiance
            predicted_class = int(prediction[0])
            proba_array = probabilities[0]
            confidence = float(np.max(proba_array))
            
            # Mapper la classe à sa représentation texte
            predicted_label = self.target_mapping.get(
                predicted_class,
                "Inconnue"
            )
            
            result = {
                'prediction': predicted_label,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'probabilities': {
                    'Bonne': float(proba_array[0]),
                    'Moyenne': float(proba_array[1]),
                    'Mauvaise': float(proba_array[2])
                },
                'input_features': {col: data.get(col) for col in self.numeric_columns + self.categorical_columns}
            }
            
            logger.info(f"Prédiction effectuée: {result['prediction']}")
            return result
        
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {e}")
            raise


def get_prediction_service() -> PredictionService:
    """Obtenir l'instance du service de prédiction"""
    return PredictionService()
