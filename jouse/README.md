# API de Prédiction de Qualité Réseau

Une API REST en Flask pour prédire la qualité d'une connexion réseau basée sur des métriques de performance.

##  Table des matières

- [Architecture](#architecture)
- [Installation](#installation)
- [Lancement du serveur](#lancement-du-serveur)
- [Endpoints](#endpoints)
- [Utilisation](#utilisation)
- [Exemples](#exemples)
- [Déploiement](#déploiement)

## ️ Architecture

```
ANN_tensor/
├── app/
│   ├── __init__.py          # Initialisation Flask
│   ├── routes.py            # Routes/Endpoints
│   └── services.py          # Logique de prédiction
├── model/
│   ├── modele_non_entraine.pkl    # Modèle ML sauvegardé
│   └── scaler.pkl                 # Normalisation MinMaxScaler
├── static/
│   ├── css/style.css        # Styles de l'interface
│   └── js/app.js            # JavaScript frontend
├── templates/
│   └── index.html           # Interface web
├── config.py                # Configuration Flask
├── run.py                   # Point d'entrée
└── requirements-api.txt     # Dépendances Python
```

##  Installation

### Prérequis
- Python 3.8+
- pip
- Virtualenv (recommandé)

### Étapes d'installation

1. **Cloner/Accéder au projet**
   ```bash
   cd /home/la-mus/ANN_tensor
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements-api.txt
   ```

##  Lancement du serveur

### Mode développement (par défaut)
```bash
python run.py
```

Le serveur sera accessible sur: `http://0.0.0.0:5000`

### Mode production
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
python run.py
```

### Avec Gunicorn (recommandé pour la production)
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 run:app
```

### Avec Waitress (alternative cross-platform)
```bash
waitress-serve --host=0.0.0.0 --port=5000 run:app
```

##  Endpoints

### 1. **Health Check** - `GET /health`
Vérifier l'état de l'API

**Réponse (200 OK):**
```json
{
  "status": "healthy",
  "message": "API Network Quality Prediction is running"
}
```

### 2. **Schéma API** - `GET /predict/schema`
Obtenir la structure des données requises

**Réponse (200 OK):**
```json
{
  "success": true,
  "schema": {
    "numeric_fields": {
      "Download (Mbps)": "float",
      "Upload (Mbps)": "float",
      "Latence (ms)": "float",
      "Jitter (ms)": "float",
      "Loss (%)": "float"
    },
    "categorical_fields": {
      "Opérateur": "string",
      "Quartier": "string",
      "Type réseau": "string"
    },
    "output_classes": ["Bonne", "Moyenne", "Mauvaise"],
    "example_request": { ... }
  }
}
```

### 3. **Prédiction** - `POST /predict`
Effectuer une prédiction de qualité réseau

**Requête (JSON):**
```json
{
  "Opérateur": "Orange",
  "Quartier": "Centre",
  "Type réseau": "5G",
  "Download (Mbps)": 100,
  "Upload (Mbps)": 50,
  "Latence (ms)": 10,
  "Jitter (ms)": 2,
  "Loss (%)": 0.1
}
```

**Réponse (200 OK):**
```json
{
  "success": true,
  "result": {
    "prediction": "Bonne",
    "predicted_class": 0,
    "confidence": 0.95,
    "probabilities": {
      "Bonne": 0.95,
      "Moyenne": 0.04,
      "Mauvaise": 0.01
    },
    "input_features": {
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
}
```

##  Utilisation

### Via l'Interface Web

1. **Ouvrir dans le navigateur:**
   ```
   http://localhost:5000
   ```

2. **Remplir le formulaire** avec les métriques réseau

3. **Cliquer sur " Prédire la Qualité"**

4. **Voir le résultat** avec probabilités et confiance

### Via Postman

1. **Créer une nouvelle requête POST**
   - URL: `http://localhost:5000/predict`
   - Headers: `Content-Type: application/json`

2. **Remplir le body (JSON raw)**
   ```json
   {
     "Opérateur": "Orange",
     "Quartier": "Centre",
     "Type réseau": "5G",
     "Download (Mbps)": 100,
     "Upload (Mbps)": 50,
     "Latence (ms)": 10,
     "Jitter (ms)": 2,
     "Loss (%)": 0.1
   }
   ```

3. **Cliquer sur Send** et voir la réponse

### Via cURL

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Opérateur": "Orange",
    "Quartier": "Centre",
    "Type réseau": "5G",
    "Download (Mbps)": 100,
    "Upload (Mbps)": 50,
    "Latence (ms)": 10,
    "Jitter (ms)": 2,
    "Loss (%)": 0.1
  }'
```

### Via Python

```python
import requests
import json

url = "http://localhost:5000/predict"
data = {
    "Opérateur": "Orange",
    "Quartier": "Centre",
    "Type réseau": "5G",
    "Download (Mbps)": 100,
    "Upload (Mbps)": 50,
    "Latence (ms)": 10,
    "Jitter (ms)": 2,
    "Loss (%)": 0.1
}

response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

##  Exemples

### Exemple 1: Excellente Connexion
```json
{
  "Opérateur": "Orange",
  "Quartier": "Centre",
  "Type réseau": "5G",
  "Download (Mbps)": 200,
  "Upload (Mbps)": 100,
  "Latence (ms)": 5,
  "Jitter (ms)": 1,
  "Loss (%)": 0
}
```

**Résultat attendu:** Bonne 

### Exemple 2: Connexion Moyenne
```json
{
  "Opérateur": "Maroc Telecom",
  "Quartier": "Tahrir",
  "Type réseau": "4G",
  "Download (Mbps)": 50,
  "Upload (Mbps)": 25,
  "Latence (ms)": 30,
  "Jitter (ms)": 5,
  "Loss (%)": 1
}
```

**Résultat attendu:** Moyenne 

### Exemple 3: Mauvaise Connexion
```json
{
  "Opérateur": "Vodafone",
  "Quartier": "Souissi",
  "Type réseau": "3G",
  "Download (Mbps)": 10,
  "Upload (Mbps)": 5,
  "Latence (ms)": 100,
  "Jitter (ms)": 20,
  "Loss (%)": 5
}
```

**Résultat attendu:** Mauvaise 

##  Déploiement

### Sur Render.com

1. **Créer un compte** sur [render.com](https://render.com)

2. **Créer un nouveau Web Service**
   - Connecter le repo GitHub
   - Build command: `pip install -r requirements-api.txt`
   - Start command: `gunicorn --workers 4 --bind 0.0.0.0:$PORT run:app`

3. **Définir les variables d'environnement**
   - `FLASK_ENV=production`
   - `FLASK_DEBUG=False`

4. **Déployer** 

### Sur Railway.app

1. **Créer un compte** sur [railway.app](https://railway.app)

2. **Connecter votre repo GitHub**

3. **Railway détectera automatiquement** Python et créera les configs

4. **Définir les variables d'environnement**

5. **Déployer** 

### Sur PythonAnywhere

1. **Créer un compte** sur [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Uploader les fichiers** du projet

3. **Créer une Web App** avec Flask

4. **Configurer le WSGI** pour pointer vers `run:app`

5. **Déployer** 

##  Notes

- Le modèle utilise **MinMaxScaler** pour la normalisation
- Les classes de sortie sont: **Bonne** (0), **Moyenne** (1), **Mauvaise** (2)
- L'API est accessible sur le réseau local (0.0.0.0)
- CORS est activé pour les requêtes cross-origin
- Le serveur supporte les requêtes concurrentes (threaded=True)

##  Debugging

### Activer les logs détaillés
```bash
export FLASK_DEBUG=True
python run.py
```

### Tester la connexion
```bash
curl http://localhost:5000/health
```

### Voir le schéma de l'API
```bash
curl http://localhost:5000/predict/schema
```

##  Licence

Ce projet est fourni à titre éducatif.

## ‍ Auteur

Développé en 2026

---

**Besoin d'aide?** Vérifiez que:
- Python 3.8+ est installé
- Les dépendances sont installées
- Le modèle et le scaler existent dans le dossier `model/`
-  Le port 5000 n'est pas bloqué/utilisé
