# Script de démarrage rapide pour l'API Flask

set -e
echo "Network Quality Prediction API"
# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier Python
echo -e "${YELLOW}Vérification des prérequis...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED} Python 3 n'est pas installé${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN} Python ${PYTHON_VERSION} trouvé${NC}"

# Créer un environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Création de l'environnement virtuel...${NC}"
    python3 -m venv venv
    echo -e "${GREEN} Environnement virtuel créé${NC}"
fi

# Activer l'environnement virtuel
echo -e "${YELLOW}Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

# Installer les dépendances
echo -e "${YELLOW}Installation des dépendances...${NC}"
pip install -r requirements-api.txt --quiet
echo -e "${GREEN} Dépendances installées${NC}"

# Vérifier les fichiers du modèle
echo -e "${YELLOW}Vérification des fichiers du modèle...${NC}"

if [ ! -f "model/modele_non_entraine.pkl" ]; then
    echo -e "${RED} Fichier model/modele_non_entraine.pkl introuvable${NC}"
    exit 1
fi

if [ ! -f "model/scaler.pkl" ]; then
    echo -e "${RED} Fichier model/scaler.pkl introuvable${NC}"
    exit 1
fi

echo -e "${GREEN} Fichiers du modèle trouvés${NC}"

# Afficher les informations de démarrage
echo ""
echo -e "${YELLOW}"
echo -e "Démarrage du serveur...${NC}"
echo ""
echo -e "${GREEN}Serveur démarré!${NC}"
echo ""
echo -e "Accédez à l'application sur:"
echo -e "  Local:          ${GREEN}http://localhost:5000${NC}"
echo -e " Réseau local:   ${GREEN}http://$(hostname -I | awk '{print $1}'):5000${NC}"
echo ""
echo -e "${YELLOW}Interface web:     http://localhost:5000${NC}"
echo -e "${YELLOW}API Endpoint:      POST http://localhost:5000/predict${NC}"
echo -e "${YELLOW}Health Check:      GET http://localhost:5000/health${NC}"
echo -e "${YELLOW}Schéma API:        GET http://localhost:5000/predict/schema${NC}"
echo ""
echo -e "${YELLOW}Pour arrêter le serveur, appuyez sur CTRL+C${NC}"
echo ""

# Démarrer l'application
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000

python run.py
