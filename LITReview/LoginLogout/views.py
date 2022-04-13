from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, InscriptionForm

from Base import models
# Create your views here.

def LoginOrInscription(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, \
                    username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                tickets = models.Ticket.objects.all().filter(user_id=request.user.id)
                return render(request, "account/HomePage.html", {'section': 'HomePage',\
                                                                 'tickets': tickets})
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/LoginOrInscription.html', {'form': form, 'section': 'LoginOrInscription'})

def Inscription(request):
    if request.method == 'POST':
        user_form = InscriptionForm(request.POST)
        if user_form.is_valid():
            # Création d'un nouvel utilisateur sans le sauvegarder
            new_user = user_form.save(commit=False)
            # Mot de passe confirmé utilisateur
            new_user.set_password(
                user_form.cleaned_data['password1'])
            # On sauvegarde maintenant le nouvel utilisateur
            new_user.save()
            form = LoginForm()
            # login et logout en-dessous A AMELIORER, N'EST PAS OPTIMAL, mais permet d'éviter bug
            # login(request, new_user)
            # logout(request)
            return render(request, 'account/LoginOrInscription.html', {'form': form, 'section': 'LoginOrInscription'})
    else:
        user_form = InscriptionForm()
    return render(request,
                            'account/Inscription.html',
                            {'user_form': user_form, 'section': 'Inscription'})


def logout_request(request):
    logout(request)
    return HttpResponseRedirect('.')
