
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone

from .models import Evenement, Inscription


class GestionEvenementsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='utilisateur_test',
            password='Test12345!'
        )

        self.evenement = Evenement.objects.create(
            titre='Conférence Django',
            description='Une conférence de programmation.',
            date=timezone.now() + timedelta(days=10),
            lieu='Antsirabe',
            capacite=2,
            categorie='Conference'
        )

    def test_places_restantes(self):
        Inscription.objects.create(
            utilisateur=self.user,
            evenement=self.evenement
        )

        self.assertEqual(
            self.evenement.places_restantes(),
            1
        )

    def test_inscription_utilisateur(self):
        self.client.login(
            username='utilisateur_test',
            password='Test12345!'
        )

        response = self.client.post(
            reverse(
                'event_register',
                args=[self.evenement.pk]
            )
        )

        self.assertRedirects(
            response,
            reverse('my_registrations')
        )

        self.assertTrue(
            Inscription.objects.filter(
                utilisateur=self.user,
                evenement=self.evenement,
                statut='confirmee'
            ).exists()
        )

    def test_capacite_maximale(self):
        autre_user = User.objects.create_user(
            username='autre',
            password='Test12345!'
        )

        Inscription.objects.create(
            utilisateur=self.user,
            evenement=self.evenement
        )

        Inscription.objects.create(
            utilisateur=autre_user,
            evenement=self.evenement
        )

        self.assertTrue(self.evenement.est_complet())

        nouveau_user = User.objects.create_user(
            username='troisieme',
            password='Test12345!'
        )

        self.client.login(
            username='troisieme',
            password='Test12345!'
        )

        self.client.post(
            reverse(
                'event_register',
                args=[self.evenement.pk]
            )
        )

        self.assertFalse(
            Inscription.objects.filter(
                utilisateur=nouveau_user,
                evenement=self.evenement
            ).exists()
        )

    def test_acces_gestionnaire_refuse_utilisateur_simple(self):
        self.client.login(
            username='utilisateur_test',
            password='Test12345!'
        )

        response = self.client.get(
            reverse('manager_dashboard')
        )

        self.assertRedirects(
            response,
            reverse('event_list')
        )

    def test_acces_gestionnaire_autorise(self):
        groupe, created = Group.objects.get_or_create(
            name='Gestionnaire'
        )

        self.user.groups.add(groupe)

        self.client.login(
            username='utilisateur_test',
            password='Test12345!'
        )

        response = self.client.get(
            reverse('manager_dashboard')
        )

        self.assertEqual(response.status_code, 200)
