
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Pages publiques
    path('', views.event_list, name='event_list'),
    path('evenement/<int:pk>/', views.event_detail, name='event_detail'),

    # Authentification
    path('inscription/', views.register, name='register'),
    path(
        'connexion/',
        auth_views.LoginView.as_view(
            template_name='events/login.html'
        ),
        name='login'
    ),
    path(
        'deconnexion/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Utilisateur
    path(
        'evenement/<int:pk>/inscrire/',
        views.event_register,
        name='event_register'
    ),
    path(
        'mes-inscriptions/',
        views.my_registrations,
        name='my_registrations'
    ),
    path(
        'inscription/<int:pk>/annuler/',
        views.cancel_registration,
        name='cancel_registration'
    ),

    # Gestionnaire
    path(
        'gestionnaire/',
        views.manager_dashboard,
        name='manager_dashboard'
    ),
    path(
        'gestionnaire/evenement/ajouter/',
        views.event_create,
        name='event_create'
    ),
    path(
        'gestionnaire/evenement/<int:pk>/modifier/',
        views.event_update,
        name='event_update'
    ),
    path(
        'gestionnaire/evenement/<int:pk>/supprimer/',
        views.event_delete,
        name='event_delete'
    ),
    path(
        'gestionnaire/evenement/<int:pk>/participants/',
        views.event_attendees,
        name='event_attendees'
    ),
]
