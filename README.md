# APPLICATION WEB DE GESTION DES INSCRIPTIONS AUX ÉVÉNEMENTS

## 1. Présentation du projet

Ce projet consiste à développer une application web avec Django permettant de gérer les inscriptions aux différents événements organisés par une association.

L'application permet aux visiteurs de consulter les événements disponibles, aux utilisateurs authentifiés de s'inscrire et de suivre leurs inscriptions, et aux gestionnaires d'administrer les événements et de consulter les participants.

### Objectifs

- Présenter les événements à venir.
- Permettre aux utilisateurs de s'inscrire aux événements.
- Éviter les inscriptions en double.
- Gérer les capacités et les places disponibles.
- Permettre l'annulation des inscriptions.
- Faciliter le suivi des participants par les gestionnaires.

## 2. Technologies utilisées

Le projet utilise les technologies suivantes :

- **Python** : langage de programmation.
- **Django** : framework de développement web.
- **SQLite** : système de gestion de base de données.
- **HTML/CSS** : création des interfaces utilisateur.
- **Bootstrap** : mise en forme des interfaces (si utilisé).
- **Git/GitHub** : gestion des versions du projet.

## 3. Prérequis

Avant de commencer l'installation, il faut disposer des éléments suivants :

- Python 3 installé sur l'ordinateur.
- pip pour installer les packages Python.
- Un éditeur de code (Visual Studio Code recommandé).
- Git pour récupérer le projet.
- Un navigateur web.

Pour vérifier l'installation de Python :

```bash
python --version
```

Pour vérifier pip :

```bash
pip --version
```

## 4. Installation du projet

### Étape 1 : Récupération du projet

Cloner le dépôt Git :

```bash
git clone https://github.com/nomenamisedratiana05/djangoProjet
```

Entrer dans le dossier du projet :

```bash
cd djangoProjet
```

### Étape 2 : Création de l'environnement virtuel

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer l'environnement virtuel sous Windows :

```powershell
venv\Scripts\activate
```


### Étape 3 : Installation des dépendances

Mettre pip à jour :

```bash
python -m pip install --upgrade pip
```

Installer les dépendances du projet :

```bash
pip install -r requirements.txt
```

Le fichier requirements.txt contient les différentes bibliothèques nécessaires au fonctionnement de l'application.

## 5. Création du projet Django (si nécessaire)

Si le projet doit être créé depuis zéro, installer Django :

```bash
pip install django
```

Créer le projet :

```bash
django-admin startproject config .
```

Créer l'application :

```bash
python manage.py startapp evenements
```

Ajouter l'application `evenements` dans `INSTALLED_APPS` du fichier `config/settings.py`.

Générer le fichier requirements.txt :

```bash
pip freeze > requirements.txt
```

## 6. Configuration de la base de données

L'application utilise SQLite comme système de gestion de base de données.

SQLite est intégré à Django et ne nécessite pas l'installation d'un serveur de base de données externe.

Dans le fichier `settings.py`, la configuration standard est :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Création de la base de données

Exécuter les migrations :

```bash
python manage.py makemigrations
```

Puis appliquer les migrations :

```bash
python manage.py migrate
```

Ces commandes permettent de créer les tables nécessaires au fonctionnement de l'application.

## 7. Création d'un compte gestionnaire

Pour accéder à l'espace d'administration Django, créer un compte administrateur :

```bash
python manage.py createsuperuser
```

Renseigner ensuite :

- Nom d'utilisateur.
- Adresse e-mail.
- Mot de passe.

Le mot de passe doit être saisi de manière sécurisée dans le terminal.

Après la création du compte, le gestionnaire peut accéder à l'administration Django à l'adresse :

`http://127.0.0.1:8000/admin/`

**Remarque :** le compte superutilisateur donne accès à l'administration Django. Si l'application utilise un rôle gestionnaire distinct, il faudra également attribuer 
les permissions correspondantes.

## 8. Lancement de l'application

Pour démarrer le serveur de développement Django :

```bash
python manage.py runserver
```

Ouvrir ensuite un navigateur et accéder à :

`http://127.0.0.1:8000/`

L'application est maintenant accessible en local.

Pour arrêter le serveur, utiliser :

```bash
CTRL + C
```

## 9. Exécution des tests automatisés

Le projet comporte des tests permettant de vérifier le bon fonctionnement des principales fonctionnalités.

Pour exécuter tous les tests :

```bash
python manage.py test
```

Les tests doivent notamment vérifier :

- La validation des données d'un événement.
- Les règles de gestion des inscriptions.
- Les restrictions d'accès entre utilisateurs et gestionnaires.

Django affiche les résultats des tests directement dans le terminal.

## 10. Structure du projet

Exemple d'organisation des fichiers :

```text
NOM_DU_PROJET/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── evenements/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── README.md
└── db.sqlite3
```

Cette structure est indicative et doit être adaptée à l'organisation réelle du projet.

## 11. Fonctionnalités principales

### Pour les visiteurs
- Consulter les événements à venir.
- Rechercher un événement.
- Consulter les détails d'un événement.

### Pour les utilisateurs authentifiés
- S'inscrire à un événement.
- Consulter leurs inscriptions.
- Annuler une inscription avant le début de l'événement.

### Pour les gestionnaires
- Créer et modifier des événements.
- Consulter la liste des participants.
- Suivre les inscriptions confirmées et annulées.
- Gérer les événements et leurs capacités.

## 12. Informations importantes

- La base de données utilisée est SQLite.
- L'application fonctionne localement sans service externe.
- Les opérations sensibles sont protégées par le système d'authentification et les permissions Django.
- Les formulaires sont validés côté serveur.
- Les opérations de modification utilisent les méthodes POST et la protection CSRF.

---

**Projet académique : Gestion des inscriptions à des événements**

**Framework : Django**

**Base de données : SQLite**
