from django.shortcuts import render, redirect

# TEST 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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
            # doit quelque part trouver comment identifier l'utilisateur et le relier à la photo
            ticket.save()
            return redirect('HomePage')
    return render(request, 'critics/ticket_creation.html', context={'form': form})


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

