from django.shortcuts import render, redirect

# TEST 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from . import models, forms
# def welcome_view(request):
#     message = f'<html><h1>Welcome to LITReview !</h1></html>'
#     return HttpResponse(message)

# FIN DU TEST

# Create your views here.
# def LoginOrInscription(request):
#     return render(request, "LoginOrInscription.html")

def InscriptionView(request):
    return None

# def HomePage(request):
#     return render(request, 'HomePage.html')

@login_required
def HomePage(request):
    tickets = models.Ticket.objects.all()
    # Il faut également que je puisse faire en sorte que l'on affiche uniquement les tickets et critiques appartenant
    # à l'utilisateur et pas plus
    return render(request,
        'account/HomePage.html', context={'tickets': tickets, 'section': 'HomePage'})

@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('HomePage')
    return render(request, 'critics/ticket_creation.html', context={'form': form})

@login_required
def review_and_ticket_upload(request):
    review_form = forms.ReviewForm
    ticket_form = forms.TicketForm
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if any(review_form.is_valid(), ticket_form.is_valid()):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('HomePage')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form
    }
    return render(request, 'critics/review_and_ticket_creation.html', context=context)


@login_required
def subscribers_page(request):
    users = User.objects.all()
    return render(request, 'subscribers_page.html', context={'users':users})
# Premier jet brouillon écriture de vues
# def MySubscriptionsView(request):
#     return None

# def TicketCreation(request):
#     # Il faut aussi pouvoir modifier un ticket
#     return None

# def TicketView(request):
#     return None

# def CriticCreation(request):
#     # Il faut aussi pouvoir mofidier une critique
#     return None

# def CriticView(request):
#     return None

