
from django.contrib import admin
from .models import Evenement, Inscription


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = (
        'titre',
        'categorie',
        'date',
        'lieu',
        'capacite',
    )
    list_filter = ('categorie', 'date')
    search_fields = ('titre', 'lieu', 'description')
    ordering = ('date',)


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'utilisateur',
        'evenement',
        'date_inscription',
        'statut',
    )
    list_filter = ('statut', 'date_inscription')
    search_fields = (
        'utilisateur__username',
        'evenement__titre',
    )
    ordering = ('-date_inscription',)
