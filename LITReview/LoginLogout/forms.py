from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'Utilisateur")
    password = forms.CharField(label="Mot de Passe", widget=forms.PasswordInput)

class InscriptionForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'Utilisateur")
    password1 = forms.CharField(label="Mot de Passe",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation Mot de Passe",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Les Mots de Passe ne sont pas identiques.')
        return cd['password2']