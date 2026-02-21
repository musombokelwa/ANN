#  Guide de Démarrage Rapide

Commencez à utiliser l'API Network Quality Prediction en 5 minutes!

## ⚡ Démarrage Ultra-Rapide (2 min)

### 1. Valider le projet
```bash
cd /home/la-mus/ANN_tensor
python validate.py
```

### 2. Lancer le serveur
```bash
# Option A: Script automatique (recommandé)
bash start.sh

# Option B: Manuel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-api.txt
python run.py
```

### 3. Accéder à l'interface web
Ouvrir dans le navigateur:
```
http://localhost:5000
```

✅ C'est fait! Vous pouvez maintenant tester l'API.

---

##  Utilisation de l'Interface Web

1. **Remplir le formulaire** avec vos métriques réseau
2. **Cliquer " Prédire la Qualité"**
3. **Voir le résultat** avec probabilités et confiance

### Exemples rapides
- Cliquer sur les cartes d'exemples pour pré-remplir le formulaire
- Modifier les valeurs et prédire à nouveau

---

##  Tests avec Postman

### Importer la collection
1. Ouvrir Postman
2. "Import" → Sélectionner `Postman_Collection.json`
3. Exécuter les requêtes

### Ou tester manuellement
**POST** `http://localhost:5000/predict`

Body JSON:
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

---

##  Tests avec Python

```bash
# Utiliser le client Python fourni
python client.py

# Ou en module Python
python3 -c "
from client import NetworkQualityAPIClient
client = NetworkQualityAPIClient()
result = client.predict({
    'Opérateur': 'Orange',
    'Quartier': 'Centre',
    'Type réseau': '5G',
    'Download (Mbps)': 100,
    'Upload (Mbps)': 50,
    'Latence (ms)': 10,
    'Jitter (ms)': 2,
    'Loss (%)': 0.1
})
print(result)
"
```

---

##  Endpoints Principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| **GET** | `/` | Page d'accueil + interface web |
| **GET** | `/health` | Vérifier que l'API fonctionne |
| **GET** | `/predict/schema` | Schéma de l'API |
| **POST** | `/predict` | Prédire la qualité réseau |

---

##  Statut du Serveur

### Vérifier que le serveur fonctionne
```bash
curl http://localhost:5000/health
```

Réponse attendue:
```json
{
  "status": "healthy",
  "message": "API Network Quality Prediction is running"
}
```

### Voir le schéma de l'API
```bash
curl http://localhost:5000/predict/schema
```

---

##  Avec Docker (Optionnel)

### Lancer avec Docker
```bash
docker-compose up -d
```

### Voir les logs
```bash
docker-compose logs -f api
```

### Arrêter
```bash
docker-compose down
```

---

##  Documentation Complète

- **API Détaillée:** Voir [API_README.md](API_README.md)
- **Déploiement Cloud:** Voir [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Configuration:** Voir [config.py](config.py)

---

## 🆘 Troubleshooting Rapide

### "Port 5000 already in use"
```bash
# Utiliser un autre port
export FLASK_PORT=5001
python run.py
```

### "Module not found"
```bash
# Réinstaller les dépendances
pip install -r requirements-api.txt
```

### "Modèle non trouvé"
```bash
# Vérifier que les fichiers existent
ls -la model/
```

### "Erreur de connexion"
```bash
# Vérifier que le serveur est lancé
curl http://localhost:5000/health
```

---

##  Cas d'Usage Courants

### Tester une connexion 5G
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Opérateur": "Orange",
    "Quartier": "Centre",
    "Type réseau": "5G",
    "Download (Mbps)": 200,
    "Upload (Mbps)": 100,
    "Latence (ms)": 5,
    "Jitter (ms)": 1,
    "Loss (%)": 0
  }'
```

### Tester une mauvaise connexion
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Opérateur": "Vodafone",
    "Quartier": "Souissi",
    "Type réseau": "3G",
    "Download (Mbps)": 10,
    "Upload (Mbps)": 5,
    "Latence (ms)": 100,
    "Jitter (ms)": 20,
    "Loss (%)": 5
  }'
```

---

##  Accès Réseau Local

L'API est accessible sur votre réseau local:
```
http://<votre-ip-locale>:5000
```

Pour trouver votre IP:
```bash
# Linux/Mac
hostname -I

# Windows
ipconfig
```

---

##  Tester sur Mobile

1. Trouver l'IP locale de votre machine
2. Accéder à: `http://<ip-locale>:5000`
3. Utiliser l'interface web sur mobile

---

## ⭐ Prochaines Étapes

1. ✅ Lancer l'API localement
2. ✅ Tester avec des exemples
3.  [Déployer en cloud](DEPLOYMENT_GUIDE.md)
4.  Intégrer dans votre application

---

## 🤝 Support

- **Documentation API:** [API_README.md](API_README.md)
- **Déploiement:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Tests:** `test_api.py`, `client.py`

---

**Besoin d'aide?** Vérifiez d'abord:
- ✅ Python 3.8+ installé
- ✅ Dépendances: `pip install -r requirements-api.txt`
- ✅ Modèle présent: `ls model/`
- ✅ Port 5000 disponible

Bon déploiement! 
