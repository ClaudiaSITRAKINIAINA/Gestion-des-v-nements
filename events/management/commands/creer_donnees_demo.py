
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone

from events.models import Evenement, Inscription


class Command(BaseCommand):
    help = "Créer les données de démonstration de l'application"

    def handle(self, *args, **options):
        maintenant = timezone.now()

        # 1. Créer ou récupérer le groupe Gestionnaire
        groupe, _ = Group.objects.get_or_create(name="Gestionnaire")

        # 2. Créer les utilisateurs de démonstration
        utilisateurs = [
            {
                "username": "participant1",
                "email": "participant1@example.com",
                "password": "Demo2026!",
            },
            {
                "username": "participant2",
                "email": "participant2@example.com",
                "password": "Demo2026!",
            },
            {
                "username": "participant3",
                "email": "participant3@example.com",
                "password": "Demo2026!",
            },
        ]

        comptes = {}

        for donnees in utilisateurs:
            user, created = User.objects.get_or_create(
                username=donnees["username"],
                defaults={"email": donnees["email"]},
            )

            if created:
                user.set_password(donnees["password"])
                user.save()

            comptes[user.username] = user

        # Ajouter le groupe Gestionnaire au compte gestionnaire
        gestionnaire = User.objects.filter(username="gestionnaire").first()

        if gestionnaire:
            gestionnaire.groups.add(groupe)

        # 3. Créer les événements
        evenements = [
            {
                "titre": "Atelier de développement Web avec Django",
                "description": "Découverte de Django, création de modèles, vues et applications Web.",
                "jours": 3,
                "lieu": "Université d'Antsirabe",
                "capacite": 30,
                "categorie": "Atelier",
            },
            {
                "titre": "Conférence sur l'intelligence artificielle",
                "description": "Présentation des applications de l'intelligence artificielle dans les entreprises.",
                "jours": 5,
                "lieu": "Salle de conférence ESP",
                "capacite": 50,
                "categorie": "Conference",
            },
            {
                "titre": "Rencontre des étudiants en informatique",
                "description": "Échanges autour des projets informatiques et des opportunités professionnelles.",
                "jours": 8,
                "lieu": "Campus universitaire",
                "capacite": 40,
                "categorie": "Rencontre",
            },
            {
                "titre": "Atelier Python et Data Science",
                "description": "Initiation à Python, à l'analyse de données et à la visualisation.",
                "jours": 12,
                "lieu": "Laboratoire informatique",
                "capacite": 25,
                "categorie": "Atelier",
            },
            {
                "titre": "Conférence sur la cybersécurité",
                "description": "Bonnes pratiques de sécurité informatique et protection des données.",
                "jours": 15,
                "lieu": "Centre de formation",
                "capacite": 60,
                "categorie": "Conference",
            },
            {
                "titre": "Rencontre des développeurs",
                "description": "Partage d'expériences entre développeurs et présentation de projets.",
                "jours": 20,
                "lieu": "Antsirabe",
                "capacite": 35,
                "categorie": "Rencontre",
            },
        ]

        objets_evenements = []

        for donnees in evenements:
            evenement, created = Evenement.objects.get_or_create(
                titre=donnees["titre"],
                defaults={
                    "description": donnees["description"],
                    "date": maintenant + timedelta(days=donnees["jours"]),
                    "lieu": donnees["lieu"],
                    "capacite": donnees["capacite"],
                    "categorie": donnees["categorie"],
                },
            )
            objets_evenements.append(evenement)

        # 4. Créer les inscriptions de démonstration
        inscriptions_demo = [
            ("participant1", 0, "confirmee"),
            ("participant2", 0, "confirmee"),
            ("participant3", 0, "confirmee"),
            ("participant1", 1, "confirmee"),
            ("participant2", 1, "confirmee"),
            ("participant3", 2, "confirmee"),
            ("participant1", 3, "confirmee"),
            ("participant2", 3, "annulee"),
            ("participant3", 4, "confirmee"),
        ]

        for username, index_evenement, statut in inscriptions_demo:
            Inscription.objects.get_or_create(
                utilisateur=comptes[username],
                evenement=objets_evenements[index_evenement],
                defaults={"statut": statut},
            )

        self.stdout.write(self.style.SUCCESS(
            "Données de démonstration créées avec succès !"
        ))
        self.stdout.write(f"Utilisateurs de démonstration : {len(comptes)}")
        self.stdout.write(
            f"Événements de démonstration : {len(objets_evenements)}"
        )
        self.stdout.write(
            f"Inscriptions enregistrées : {Inscription.objects.count()}"
        )
