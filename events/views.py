
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Evenement, Inscription
from .forms import InscriptionUtilisateurForm, EvenementForm


# =====================================================
# PERMISSIONS GESTIONNAIRE
# =====================================================

def gestionnaire_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        autorise = (
            request.user.is_staff
            or request.user.groups.filter(
                name='Gestionnaire'
            ).exists()
        )

        if not autorise:
            messages.error(
                request,
                "Accès réservé aux gestionnaires."
            )
            return redirect('event_list')

        return view_func(request, *args, **kwargs)

    return wrapper


# =====================================================
# ACCUEIL : LISTE, RECHERCHE, FILTRE, PAGINATION
# =====================================================

def event_list(request):
    evenements = Evenement.objects.filter(
        date__gt=timezone.now()
    ).order_by('date')

    recherche = request.GET.get('q', '').strip()
    categorie = request.GET.get('categorie', '').strip()

    if recherche:
        evenements = evenements.filter(
            titre__icontains=recherche
        )

    categories_valides = [
        choix[0] for choix in Evenement.CATEGORIES
    ]

    if categorie in categories_valides:
        evenements = evenements.filter(
            categorie=categorie
        )

    paginator = Paginator(evenements, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'events/event_list.html',
        {
            'page_obj': page_obj,
            'recherche': recherche,
            'categorie': categorie,
            'categories': Evenement.CATEGORIES,
        }
    )


# =====================================================
# DETAIL D'UN EVENEMENT
# =====================================================

def event_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)

    inscription = None

    if request.user.is_authenticated:
        inscription = Inscription.objects.filter(
            utilisateur=request.user,
            evenement=evenement
        ).first()

    return render(
        request,
        'events/event_detail.html',
      {
    'evenement': evenement,
    'inscription': inscription,
    'now': timezone.now(),
      }
    )


# =====================================================
# INSCRIPTION / CONNEXION / DECONNEXION
# =====================================================

def register(request):
    if request.user.is_authenticated:
        return redirect('event_list')

    if request.method == 'POST':
        form = InscriptionUtilisateurForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Votre compte a été créé avec succès."
            )

            return redirect('event_list')
    else:
        form = InscriptionUtilisateurForm()

    return render(
        request,
        'events/register.html',
        {'form': form}
    )


# =====================================================
# INSCRIPTION A UN EVENEMENT
# =====================================================

@login_required
@require_POST
def event_register(request, pk):

    with transaction.atomic():
        evenement = get_object_or_404(
            Evenement.objects.select_for_update(),
            pk=pk
        )

        if evenement.date <= timezone.now():
            messages.error(
                request,
                "Cet événement est déjà passé ou a commencé."
            )
            return redirect('event_detail', pk=pk)

        inscription = Inscription.objects.filter(
            utilisateur=request.user,
            evenement=evenement
        ).first()

        if inscription and inscription.statut == 'confirmee':
            messages.warning(
                request,
                "Vous êtes déjà inscrit à cet événement."
            )
            return redirect('event_detail', pk=pk)

        places = evenement.places_restantes()

        if places <= 0:
            messages.error(
                request,
                "Désolé, cet événement est complet."
            )
            return redirect('event_detail', pk=pk)

        if inscription:
            inscription.statut = 'confirmee'
            inscription.date_inscription = timezone.now()
            inscription.save(
                update_fields=['statut', 'date_inscription']
            )
        else:
            Inscription.objects.create(
                utilisateur=request.user,
                evenement=evenement,
                statut='confirmee'
            )

    messages.success(
        request,
        "Votre inscription est confirmée !"
    )

    return redirect('my_registrations')


# =====================================================
# ANNULATION D'UNE INSCRIPTION
# =====================================================

@login_required
@require_POST
def cancel_registration(request, pk):

    inscription = get_object_or_404(
        Inscription,
        pk=pk,
        utilisateur=request.user
    )

    if inscription.evenement.date <= timezone.now():
        messages.error(
            request,
            "Vous ne pouvez plus annuler cette inscription."
        )
    elif inscription.statut == 'annulee':
        messages.warning(
            request,
            "Cette inscription est déjà annulée."
        )
    else:
        inscription.statut = 'annulee'
        inscription.save(update_fields=['statut'])

        messages.success(
            request,
            "Votre inscription a été annulée."
        )

    return redirect('my_registrations')


# =====================================================
# ESPACE PERSONNEL UTILISATEUR
# =====================================================

@login_required
def my_registrations(request):

    inscriptions = Inscription.objects.filter(
        utilisateur=request.user
    ).select_related('evenement').order_by(
        '-date_inscription'
    )

    return render(
        request,
        'events/my_registrations.html',
        {
    'inscriptions': inscriptions,
    'now': timezone.now(),
        }
    )


# =====================================================
# TABLEAU DE BORD GESTIONNAIRE
# =====================================================

@gestionnaire_required
def manager_dashboard(request):

    evenements = Evenement.objects.all().order_by('-date')

    context = {
        'evenements': evenements,
        'total_evenements': evenements.count(),
        'total_inscriptions': Inscription.objects.count(),
        'total_confirmees': Inscription.objects.filter(
            statut='confirmee'
        ).count(),
        'total_annulees': Inscription.objects.filter(
            statut='annulee'
        ).count(),
    }

    return render(
        request,
        'events/manager_dashboard.html',
        context
    )


# =====================================================
# CREATION EVENEMENT
# =====================================================

@gestionnaire_required
def event_create(request):

    if request.method == 'POST':
        form = EvenementForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Événement créé avec succès."
            )

            return redirect('manager_dashboard')
    else:
        form = EvenementForm()

    return render(
        request,
        'events/event_form.html',
        {
            'form': form,
            'titre_page': 'Créer un événement',
        }
    )


# =====================================================
# MODIFICATION EVENEMENT
# =====================================================

@gestionnaire_required
def event_update(request, pk):

    evenement = get_object_or_404(Evenement, pk=pk)

    if request.method == 'POST':
        form = EvenementForm(
            request.POST,
            instance=evenement
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Événement modifié avec succès."
            )

            return redirect('manager_dashboard')
    else:
        form = EvenementForm(instance=evenement)

    return render(
        request,
        'events/event_form.html',
        {
            'form': form,
            'titre_page': 'Modifier un événement',
        }
    )


# =====================================================
# SUPPRESSION EVENEMENT
# =====================================================

@gestionnaire_required
@require_POST
def event_delete(request, pk):

    evenement = get_object_or_404(Evenement, pk=pk)
    evenement.delete()

    messages.success(
        request,
        "Événement supprimé avec succès."
    )

    return redirect('manager_dashboard')


# =====================================================
# PARTICIPANTS D'UN EVENEMENT
# =====================================================

@gestionnaire_required
def event_attendees(request, pk):

    evenement = get_object_or_404(Evenement, pk=pk)

    inscriptions = Inscription.objects.filter(
        evenement=evenement
    ).select_related('utilisateur').order_by(
        '-date_inscription'
    )

    return render(
        request,
        'events/event_attendees.html',
        {
            'evenement': evenement,
            'inscriptions': inscriptions,
        }
    )
