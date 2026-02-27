# Guide de Déploiement Cloud

Ce document explique comment déployer l'API sur différentes plateformes cloud.

##  Table des matières

- [Render.com](#rendercom)
- [Railway.app](#railwayapp)
- [PythonAnywhere](#pythonanywhere)
- [Heroku (Alternative)](#heroku-alternative)

---

##  Render.com

### Avantages
- Déploiement gratuit (plan free avec limitations)
- Déploiement automatique depuis GitHub
- Support natif Flask
- Configuration simple

### Étapes

1. **Créer un compte** sur [render.com](https://render.com)

2. **Connecter votre repo GitHub**
   - Cliquer sur "New+" → "Web Service"
   - Sélectionner votre repo
   - Autoriser l'accès à GitHub

3. **Configurer le service**
   ```
   Name: network-quality-api
   Runtime: Python 3
   Build Command: pip install -r requirements-api.txt
   Start Command: gunicorn --workers 4 --bind 0.0.0.0:$PORT run:app
   ```

4. **Variables d'environnement**
   - Aller à "Environment"
   - Ajouter:
     ```
     FLASK_ENV=production
     FLASK_DEBUG=False
     SECRET_KEY=your-long-random-secret-key
     ```

5. **Déployer**
   - Cliquer sur "Create Web Service"
   - Attendre ~2-3 minutes
   - L'URL sera générée automatiquement

### URL de production
```
https://network-quality-api.onrender.com
```

### Coûts
- Plan gratuit: 15$ de crédits/mois (suffisant pour une petite API)
- Plan payant: À partir de 7$/mois

---

##  Railway.app

### Avantages
- Déploiement très simplifié
- Docker support natif
- Détection automatique du langage
- Plan gratuit généreux

### Étapes

1. **Créer un compte** sur [railway.app](https://railway.app)

2. **Connecter GitHub**
   - Cliquer sur "New Project"
   - "Deploy from GitHub repo"
   - Sélectionner votre repo

3. **Railway détectera automatiquement**
   - Python
   - requirements-api.txt
   - Configurera Gunicorn

4. **Ajouter des variables d'environnement**
   - Aller à "Variables"
   - Ajouter:
     ```
     FLASK_ENV=production
     PORT=5000
     SECRET_KEY=your-secret-key
     ```

5. **Déploiement automatique**
   - Railway déploie automatiquement à chaque push

### URL de production
```
https://<project-name>.railway.app
```

### Coûts
- Plan gratuit: $5/mois de crédit
- Plan payant: $20/mois (illimité)

---

##  PythonAnywhere

### Avantages
- Plateforme Python dédiée
- Gratuit avec limitations
- Interface web simple
- Support direct Python

### Étapes

1. **Créer un compte** sur [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Uploader les fichiers**
   - Menu "Files"
   - Créer dossier: `network-quality-api`
   - Uploader les fichiers du projet

3. **Créer une virtualenv**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements-api.txt
   ```

4. **Créer une Web App**
   - Menu "Web"
   - "Add a new web app"
   - Sélectionner "Flask"
   - Sélectionner Python 3.10

5. **Configurer WSGI**
   - Éditer le fichier WSGI généré: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Remplacer par:
   ```python
   import sys
   path = '/home/yourusername/network-quality-api'
   if path not in sys.path:
       sys.path.append(path)
   
   from run import app
   application = app
   ```

6. **Recharger l'application**
   - Menu "Web"
   - Cliquer sur "Reload yourusername.pythonanywhere.com"

### URL de production
```
https://yourusername.pythonanywhere.com
```

### Coûts
- Plan gratuit: API limitée (généraux)
- Plan payant: À partir de $5/mois

---

##  Heroku (Alternative)

**Note:** Heroku a arrêté le plan gratuit en novembre 2022, mais reste une option payante.

### Étapes rapides

1. **Créer un compte** sur [heroku.com](https://www.heroku.com)

2. **Installer Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

3. **Ajouter un fichier Procfile**
   ```
   web: gunicorn run:app
   ```

4. **Déployer**
   ```bash
   heroku login
   heroku create network-quality-api
   git push heroku main
   ```

### Coûts
- Dynos: À partir de $7/mois

##  Sécurité en Production

Avant de déployer, assurez-vous:

1. **SECRET_KEY unique et fort**
   ```bash
   python -c 'import secrets; print(secrets.token_hex(32))'
   ```

2. **FLASK_ENV = production**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

3. **CORS configuré correctement**
   ```python
   CORS(app, resources={
       r"/predict": {"origins": ["yourdomain.com"]}
   })
   ```

4. **Certificat SSL/TLS**
   - Render, Railway, PythonAnywhere fournissent HTTPS gratuit
   - Heroku aussi inclus

5. **Monitoring**
   - Activer les logs
   - Mettre en place des alertes

---

## 🧪 Tester le Déploiement

Une fois déployé, tester les endpoints:

```bash
# Health check
curl https://<your-app>.com/health

# Schéma API
curl https://<your-app>.com/predict/schema

# Prédiction
curl -X POST https://<your-app>.com/predict \
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

---

##  Troubleshooting

### Application s'arrête après le déploiement
- Vérifier les logs: `render logs` ou `railway logs`
- S'assurer que le modèle et le scaler existent
- Vérifier requirements-api.txt

### Port non accessible
- S'assurer que FLASK_HOST=0.0.0.0
- Bind port = $PORT (Render/Railway)

### Modèle/Scaler non trouvés
- S'assurer que les fichiers sont uploadés
- Vérifier les chemins dans app/services.py
- Utiliser des chemins relatifs

### Timeout
- Augmenter le timeout Gunicorn: `--timeout 60`
- Vérifier la taille du modèle
- Vérifier la RAM disponible

---

##  Ressources

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [PythonAnywhere Help](https://help.pythonanywhere.com)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)

---

##  Prochaines étapes

Après le déploiement:

1. Configurer un domaine personnalisé
2. Mettre en place le monitoring (Sentry, DataDog)
3. Ajouter l'authentification (JWT)
4. Configurer CI/CD (GitHub Actions)
5. Ajouter des tests automatisés

---

Bon déploiement! 
