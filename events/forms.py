
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Evenement


# =====================================================
# FORMULAIRE DE CREATION DE COMPTE
# =====================================================

class InscriptionUtilisateurForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Adresse e-mail"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


# =====================================================
# FORMULAIRE DE CREATION ET MODIFICATION D'EVENEMENT
# =====================================================

class EvenementForm(forms.ModelForm):

    date = forms.DateTimeField(
        label="Date et heure",
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Evenement

        fields = [
            'titre',
            'description',
            'date',
            'lieu',
            'capacite',
            'categorie',
            'image',
        ]

        widgets = {
            'titre': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'class': 'form-control'
                }
            ),
            'lieu': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'capacite': forms.NumberInput(
                attrs={
                    'min': 1,
                    'class': 'form-control'
                }
            ),
            'categorie': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs.update({
                    'class': 'form-control'
                })

        self.fields['image'].required = False
        self.fields['image'].label = "Image de l'événement"

    def clean_date(self):
        date = self.cleaned_data['date']

        if date <= timezone.now():
            raise forms.ValidationError(
                "La date de l'événement doit être dans le futur."
            )

        return date

    def clean_capacite(self):
        capacite = self.cleaned_data['capacite']

        if capacite < 1:
            raise forms.ValidationError(
                "La capacité doit être supérieure à zéro."
            )

        return capacite

    def clean(self):
        cleaned_data = super().clean()
        capacite = cleaned_data.get('capacite')

        if self.instance.pk and capacite is not None:

            inscriptions = self.instance.inscriptions.filter(
                statut='confirmee'
            ).count()

            if capacite < inscriptions:
                self.add_error(
                    'capacite',
                    "La capacité ne peut pas être inférieure "
                    "au nombre d'inscriptions confirmées."
                )

        return cleaned_data
