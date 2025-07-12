# cartographielocal

cartographielocal est une application dédiée à la récupération des entreprises, des emplois, de leurs informations et de leur localisation. Elle permet d’extraire, de consulter et de manipuler ces données via une API.

---

## Fonctionnalités principales

- Récupération des entreprises et de leurs informations détaillées
- Récupération des offres d’emploi associées
- Récupération des entreprises et emplois présents dans un périmètre géographique donné (fonctionnalité de géolocalisation)

---

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Un environnement virtuel Python (recommandé)

---

## Installation et utilisation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/cartographielocal.git
cd cartographielocal
```

### 2. Créer et activer un environnement virtuel (recommandé)

Sous Windows :
```bash
python -m venv venv
venv\Scripts\activate
```

Sous macOS/Linux :
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de l’environnement

Créez un fichier `.env` à la racine du projet si besoin, et renseignez-y vos variables d’environnement (exemple : clés API, configuration de la base de données, etc.).  
Exemple de contenu :
```
DATABASE_URL=sqlite:///cartographielocal.db
SECRET_KEY=une_clé_secrète
```

### 5. Lancer l’application en local

```bash
python app.py
```

L’API sera accessible à l’adresse http://localhost:5000 (ou le port configuré).

---

## Structure du projet

```
cartographielocal/
│
├── app.py                # Point d’entrée principal de l’application
├── config.py             # Configuration de l’application
├── extensions.py         # Extensions et initialisations (ex : base de données)
├── models/               # Modèles de données (company, job, location)
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

---

## Commandes utiles

- Installer les dépendances : `pip install -r requirements.txt`
- Lancer l’application : `python app.py`
- Activer l’environnement virtuel : `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/macOS)

---

## Tests unitaires

Des tests unitaires sont présents pour vérifier le bon fonctionnement des principales fonctionnalités, notamment la gestion des entreprises. Ils permettent de prévenir les régressions et de garantir la qualité du logiciel.

### Lancer les tests

1. Assurez-vous d’avoir installé les dépendances (voir plus haut).
2. Exécutez la commande suivante à la racine du projet :

```bash
pytest
```

Pour obtenir un rapport de couverture :

```bash
pytest --cov=models --cov=app
```

Les tests se trouvent dans le dossier `tests/`.