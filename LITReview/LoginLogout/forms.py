from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", \
                                                                'style': 'text-align: center;width: 400px'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': "Mot de Passe", \
                                                                'style': 'text-align: center;width: 400px'}))

class InscriptionForm(forms.ModelForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", \
                                                                'style': 'text-align: center;width: 400px'}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': "Mot de Passe", \
                                                                'style': 'text-align: center;width: 400px'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': "Confirmer Mot de Passe", \
                                                                'style': 'text-align: center;width: 400px'}))

    class Meta:
        model = User
        fields = ('username',)


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Les Mots de Passe ne sont pas identiques.')
        return cd['password2']