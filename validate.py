#!/usr/bin/env python
"""
Script de validation du projet
Vérifie que tous les fichiers et dossiers nécessaires sont présents
"""

import os
import sys
from pathlib import Path


class ProjectValidator:
    """Validateur de structure du projet"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.success = []
    
    def validate(self):
        """Lancer la validation complète"""
        print("\n" + "="*60)
        print(" Validation du Projet Network Quality Prediction")
        print("="*60 + "\n")
        
        # Vérifier les fichiers critiques
        self._check_critical_files()
        
        # Vérifier les dossiers
        self._check_directories()
        
        # Vérifier les fichiers du modèle
        self._check_model_files()
        
        # Afficher les résultats
        self._print_results()
        
        # Retourner le status
        return len(self.errors) == 0
    
    def _check_critical_files(self):
        """Vérifier les fichiers critiques"""
        print(" Vérification des fichiers critiques...")
        
        critical_files = [
            "run.py",
            "config.py",
            "requirements-api.txt",
            "Dockerfile",
            "docker-compose.yml",
        ]
        
        for file in critical_files:
            file_path = self.project_root / file
            if file_path.exists():
                self.success.append(f"✅ {file}")
            else:
                self.errors.append(f"❌ {file} - MANQUANT")
    
    def _check_directories(self):
        """Vérifier les dossiers"""
        print(" Vérification des répertoires...")
        
        required_dirs = [
            "app",
            "model",
            "templates",
            "static",
            "static/css",
            "static/js",
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.success.append(f"✅ {dir_name}/")
            else:
                self.errors.append(f"❌ {dir_name}/ - MANQUANT")
    
    def _check_model_files(self):
        """Vérifier les fichiers du modèle"""
        print("🤖 Vérification des fichiers du modèle...")
        
        model_files = [
            "model/modele_non_entraine.pkl",
            "model/scaler.pkl",
        ]
        
        for file in model_files:
            file_path = self.project_root / file
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024*1024)
                self.success.append(f"✅ {file} ({size_mb:.2f} MB)")
            else:
                self.errors.append(f"❌ {file} - MANQUANT")
    
    def _print_results(self):
        """Afficher les résultats de la validation"""
        print("\n" + "="*60)
        print(" Résultats de la Validation")
        print("="*60 + "\n")
        
        if self.success:
            print("✅ Fichiers trouvés:")
            for item in self.success:
                print(f"   {item}")
        
        if self.warnings:
            print("\n⚠️  Avertissements:")
            for item in self.warnings:
                print(f"   {item}")
        
        if self.errors:
            print("\n❌ Erreurs:")
            for item in self.errors:
                print(f"   {item}")
        
        print("\n" + "="*60)
        if not self.errors:
            print("✅ VALIDATION RÉUSSIE - Projet prêt à démarrer!")
        else:
            print(f"❌ VALIDATION ÉCHOUÉE - {len(self.errors)} erreur(s) détectée(s)")
        print("="*60 + "\n")
    
    def check_python_version(self):
        """Vérifier la version de Python"""
        print(" Vérification de Python...")
        
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            self.success.append(f"✅ Python {version.major}.{version.minor}.{version.micro}")
            return True
        else:
            self.errors.append(f"❌ Python {version.major}.{version.minor} - Minimum requis: 3.8")
            return False
    
    def check_dependencies(self):
        """Vérifier les dépendances Python"""
        print(" Vérification des dépendances Python...")
        
        required_packages = [
            "flask",
            "flask_cors",
            "numpy",
            "pandas",
            "scikit_learn",
            "joblib",
            "tensorflow",
            "keras",
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                self.success.append(f"✅ {package}")
            except ImportError:
                self.warnings.append(f"⚠️  {package} - non installé")


def main():
    """Fonction principale"""
    validator = ProjectValidator()
    
    # Vérifier Python
    validator.check_python_version()
    
    # Valider le projet
    is_valid = validator.validate()
    
    # Vérifier les dépendances (optionnel)
    print("\n" + "="*60)
    validator.check_dependencies()
    validator._print_results()
    
    # Retourner le status
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
