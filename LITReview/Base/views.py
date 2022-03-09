from django.shortcuts import render

# TEST 
from django.http import HttpResponse

def welcome_view(request):
    message = f'<html><h1>Welcome to LITReview !</h1></html>'
    return HttpResponse(message)

# FIN DU TEST

# Create your views here.
def LoginOrInscription(request):
    return render(request, "LoginOrInscription.html")

def InscriptionView(request):
    return None

def HomePage(request):
    return render(request, 'HomePage.html')

def MySubscriptionsView(request):
    return None

def TicketCreation(request):
    # Il faut aussi pouvoir modifier un ticket
    return None

def TicketView(request):
    return None

def CriticCreation(request):
    # Il faut aussi pouvoir mofidier une critique
    return None

def CriticView(request):
    return None

