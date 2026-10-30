
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Evenement(models.Model):

    CATEGORIES = [
        ('Atelier', 'Atelier'),
        ('Conference', 'Conférence'),
        ('Rencontre', 'Rencontre'),
    ]

    titre = models.CharField(max_length=200)

    description = models.TextField()

    date = models.DateTimeField()

    lieu = models.CharField(max_length=200)

    capacite = models.PositiveIntegerField()

    categorie = models.CharField(
        max_length=30,
        choices=CATEGORIES
    )

    image = models.ImageField(
    upload_to='evenements/',
    blank=True,
    null=True
    )
    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.titre

    def places_restantes(self):
        inscriptions_confirmees = self.inscriptions.filter(
            statut='confirmee'
        ).count()

        return max(0, self.capacite - inscriptions_confirmees)

    def est_complet(self):
        return self.places_restantes() <= 0

    def est_passe(self):
        return self.date <= timezone.now()


class Inscription(models.Model):

    STATUTS = [
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ]

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )

    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )

    date_inscription = models.DateTimeField(
        auto_now_add=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='confirmee'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['utilisateur', 'evenement'],
                name='inscription_unique_utilisateur_evenement'
            )
        ]
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.evenement.titre}"
