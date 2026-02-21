#!/usr/bin/env python3
"""
Script pour créer un modèle entraîné de test
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

print("🤖 Création d'un modèle entraîné pour les tests...\n")

# Créer des données d'entraînement simulées
print(" Génération de données synthétiques...")
np.random.seed(42)

# 200 samples
n_samples = 200

# Colonnes numériques: Download, Upload, Latence, Jitter, Loss
X_numeric = np.random.rand(n_samples, 5) * 200  # Valeurs entre 0-200

# Colonnes catégoriques encodées: Opérateur, Quartier, Type réseau  
X_categorical = np.random.randint(0, 50, size=(n_samples, 3))

# Combiner
X = np.hstack([X_categorical, X_numeric]).astype('float32')

# Créer les labels cibles (0: Bonne, 1: Moyenne, 2: Mauvaise)
# Logique simple: répartir les 3 classes uniformément
y = np.array([i % 3 for i in range(n_samples)], dtype='int32')
np.random.shuffle(y)

print(f"✅ {n_samples} samples créés")
print(f"   Classes: Bonne={sum(y==0)}, Moyenne={sum(y==1)}, Mauvaise={sum(y==2)}\n")

# Entraîner le modèle
print(" Entraînement du modèle RandomForest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)
print("✅ Modèle entraîné!\n")

# Créer et entraîner le scaler
print(" Création du Scaler...")
scaler = MinMaxScaler()
scaler.fit(X[:, 3:8])  # Normaliser les colonnes numériques (indices 3-8)
print("✅ Scaler créé!\n")

# Sauvegarder
model_path = 'model/modele_non_entraine.pkl'
scaler_path = 'model/scaler.pkl'

print(" Sauvegarde des fichiers...")
joblib.dump(model, model_path)
print(f"   ✅ {model_path}")

joblib.dump(scaler, scaler_path)
print(f"   ✅ {scaler_path}\n")

# Test rapide
print("🧪 Test du modèle...")
# 3 catégories (Opérateur, Quartier, Type réseau) + 5 numériques (Download, Upload, Latence, Jitter, Loss)
test_data = np.array([
    [10, 20, 100, 50, 10, 2, 0.1, 5]  # 8 colonnes totales
], dtype='float32')

test_categorical = test_data[:, :3]
test_numeric = test_data[:, 3:]

# Normaliser les colonnes numériques
test_numeric_scaled = scaler.transform(test_numeric)

# Recombiner: catégories + numériques normalisées
test_data_scaled = np.hstack([test_categorical, test_numeric_scaled])

prediction = model.predict(test_data_scaled)
proba = model.predict_proba(test_data_scaled)

classes = ['Bonne', 'Moyenne', 'Mauvaise']
predicted_class = prediction[0]

print(f"   Prédiction: {classes[predicted_class]}")
print(f"   Probabilités: Bonne={proba[0][0]:.2%}, Moyenne={proba[0][1]:.2%}, Mauvaise={proba[0][2]:.2%}")
print("\n✅ Modèle prêt à l'emploi!")
