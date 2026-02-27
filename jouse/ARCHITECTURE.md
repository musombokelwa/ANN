# ️ Architecture de l'Application

Documentation de l'architecture et du design de l'API Network Quality Prediction.

##  Vue d'Ensemble

```
┌─────────────────────────────────────────────┐
│           Client (Navigateur/Postman)       │
└────────────────┬────────────────────────────┘
                 │ HTTP/JSON
                 ▼
┌─────────────────────────────────────────────┐
│      Flask Application (run.py)             │
├─────────────────────────────────────────────┤
│ • Routes (app/routes.py)                    │
│ • CORS activé                               │
│ • Configuration (config.py)                 │
└────────────────┬────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
    ┌────────────┐  ┌──────────────┐
    │ Services   │  │ Static Files │
    │ (rédiction)│  │ (HTML/CSS/JS)│
    └────┬───────┘  └──────────────┘
         │
         ├─── Charger Modèle
         ├─── Charger Scaler
         └─── Prédiction ML
         
         ▼
    ┌──────────────┐
    │ Dossier model│
    │ • .pkl files │
    └──────────────┘
```

##  Structure des Fichiers

```
ANN_tensor/
│
├── run.py                      #  Point d'entrée principal
│
├── config.py                   #  Configuration Flask
│
├── requirements-api.txt        #  Dépendances Python
│
├── Dockerfile                  #  Configuration Docker
├── docker-compose.yml          #  Docker Compose
│
├── app/                        #  Application Flask
│   ├── __init__.py             #    Initialisation & factory
│   ├── routes.py               #    Endpoints API
│   └── services.py             #    Logique métier
│
├── model/                      # Modèle ML
│   ├── modele_non_entraine.pkl #    Modèle Random Forest
│   └── scaler.pkl              #    MinMaxScaler
│
├── templates/                  #  Frontend
│   └── index.html              #    Interface web
│
├── static/                     #  Ressources statiques
│   ├── css/
│   │   └── style.css           #    Styles
│   └── js/
│       └── app.js              #    JavaScript interactif
│
├── test/                       # Tests
│   └── test_api.py             #    Tests unitaires
│
├── scripts/                    #  Utilitaires
│   ├── start.sh                #    Script de démarrage
│   ├── client.py               #    Client Python
│   └── validate.py             #    Validateur de projet
│
└── docs/                       #  Documentation
    ├── API_README.md           #    API complète
    ├── DEPLOYMENT_GUIDE.md     #    Déploiement cloud
    ├── QUICK_START.md          #    Démarrage rapide
    └── ARCHITECTURE.md         #    Ce fichier
```

##  Flux de la Requête

```
1. Client envoie POST /predict
   └── JSON avec métriques réseau

2. Flask route handler (routes.py)
   ├── Valide Content-Type JSON
   ├── Parse le JSON
   └── Vérifie les données

3. Service de prédiction (services.py)
   ├── Prétraite les données
   │   ├── Sipse catégories
   │   └── Normalise (MinMaxScaler)
   ├── Charge le modèle (Singleton)
   └── Effectue la prédiction
       └── Random Forest classification

4. Retours des résultats
   ├── Prédiction (classe)
   ├── Confiance (probabilité)
   └── Probabilités détaillées

5. Client reçoit JSON
   └── Affiche du résultat
```

##  Endpoints API

### Hiérarchie des Routes

```
GET  /                          # Page d'accueil
GET  /health                    # Health check
GET  /predict/schema            # Schéma de l'API
POST /predict                   # Prédiction principale
```

##  Composants Clés

### 1. **app/__init__.py** - Application Factory
Crée l'instance Flask avec:
- Configuration dynamique (dev/prod)
- CORS activé
- Blueprints enregistrés
- Errorhandlers configurés

```python
def create_app(config_name='development'):
    app = Flask(__name__)
    # Configuration
    # Blueprints
    return app
```

### 2. **app/routes.py** - Endpoints
Définit les routes de l'API:
- `GET /health` - Vérification de santé
- `GET /predict/schema` - Schéma
- `POST /predict` - Prédiction
- `GET /api/test` - Test

### 3. **app/services.py** - Logique Métier
Service singleton pour:
- Charger le modèle ML (une seule fois)
- Prétraiter les données entrantes
- Effectuer les prédictions
- Mapper les résultats

Pattern Singleton:
```python
class PredictionService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 4. **templates/index.html** - Interface Web
Interface HTML5 avec:
- Formulaire avec 3 champs catégoriques
- 5 champs numériques
- Cartes d'exemples
- Affichage des résultats en temps réel

### 5. **static/css/style.css** - Styling
Gradient violet moderne avec:
- Design responsive (mobile-first)
- Animations fluides
- Thème adaptatif

### 6. **static/js/app.js** - Frontend
JavaScript pour:
- Valider le formulaire
- Appels AJAX à l'API
- Affichage des résultats
- Exemples pré-remplis

## 🤖 Pipeline ML

```
Données entrantes
    ↓
┌─ Validation ─┐
│   • Colonnes │
│   • Types    │
└──────┬───────┘
       ↓
┌─ Prétraitement ─┐
│ • Normalisation  │ (MinMaxScaler)
│   [0, 1]        │
└──────┬──────────┘
       ↓
┌───────────────┐
│ RandomForest  │ (n_estimators=100)
│ Classification│
└──────┬────────┘
       ↓
┌──────────────────┐
│ Prédiction       │
│ • Classe (0,1,2) │
│ • Probabilité    │
│ • Confiance      │
└──────────────────┘
```

##  Données

### Entrée
```json
{
  "Opérateur": "string",           # Catégorie
  "Quartier": "string",            # Catégorie
  "Type réseau": "string",         # Catégorie
  "Download (Mbps)": float,        # Numérique
  "Upload (Mbps)": float,          # Numérique
  "Latence (ms)": float,           # Numérique
  "Jitter (ms)": float,            # Numérique
  "Loss (%)": float                # Numérique
}
```

### Sortie
```json
{
  "prediction": "Bonne",           # 0: Bonne, 1: Moyenne, 2: Mauvaise
  "predicted_class": 0,            # Index classe
  "confidence": 0.95,              # [0, 1]
  "probabilities": {
    "Bonne": 0.95,
    "Moyenne": 0.04,
    "Mauvaise": 0.01
  },
  "input_features": { ... }
}
```

##  Gestion des Erreurs

```
┌─────────────────────────┐
│   Request Error         │
├─────────────────────────┤
│ • 400: Bad Request      │
│ • 404: Not Found        │
│ • 405: Method Not Allow │
│ • 500: Internal Error   │
└─────────────────────────┘
```

##  Déploiement

### Développement (localhost)
```bash
FLASK_ENV=development
FLASK_DEBUG=True
python run.py  # Port 5000
```

### Production (Cloud)
```bash
FLASK_ENV=production
gunicorn --workers 4 run:app  # Port 5000
```

### Docker
```bash
docker-compose up -d
```

##  Performance

### Optimisations
- **Singleton Pattern:** Modèle chargé une seule fois
- **Threading:** Requêtes concurrentes supportées
- **Caching:** Scaler en mémoire
- **Connection Pooling:** Requests session réutilisée

### Métriques
- Temps de réponse: ~100-200ms
- Throughput: ~10+ req/sec (machine locale)
- Mémoire: ~500MB-1GB (modèle inclus)

## Tests

### Tests Unitaires
```bash
pytest test_api.py -v
```

Tests couvrant:
- Health check
- Schema retrieval
- Valid predictions
- Error handling
- Invalid inputs

### Tests Manuels
```bash
python client.py      # Client interactif
python validate.py    # Validation projet
```

##  Configuration

### Variables d'Environnement
```bash
FLASK_ENV=development|production
FLASK_DEBUG=True|False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=random-secret
```

### Fichiers de Configuration
- `config.py` - Configuration Flask
- `requirements-api.txt` - Dépendances
- `Dockerfile` - Conteneurisation
- `.env.example` - Variables

##  Dépendances

### Principales
- **Flask** - Framework web
- **TensorFlow/Keras** - Réseau de neurones
- **scikit-learn** - ML (Random Forest)
- **pandas/numpy** - Data processing
- **joblib** - Sérialisation modèle

### Déploiement
- **Gunicorn** - WSGI server
- **docker** - Conteneurisation
- **python-dotenv** - Environment vars

##  CORS

CORS est **activé** pour:
- Requêtes web cross-origin
- Développement frontend indépendant
- Consommateurs API externes

Configuration:
```python
CORS(app)  # Accepte toutes les origines
```

##  Sécurité

### Implémentée
-  Input validation
-  CORS configuration
-  Error handling sans leaks
-  SECRET_KEY pour sessions

### À considérer pour prod
-  Rate limiting
-  API authentication (JWT)
-  HTTPS/TLS
-  Monitoring/Logging
-  Database persistence

##  Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn ML](https://scikit-learn.org/)
- [TensorFlow](https://www.tensorflow.org/)
- [Docker](https://docs.docker.com/)

---

**Architecture Version:** 1.0
**Dernière mise à jour:** 2026-02-20

