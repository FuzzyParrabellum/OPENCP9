from django.shortcuts import render, redirect

# TEST 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

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
    # la ligne ci-dessous permet de récupérer une liste de tous les utilisateurs SAUF l'utilisateur connecté actuel
    users = User.objects.exclude(id = request.user.id)
    # ceci est un test pour voir si on peut bien séparer les users abonnés et non abonnés avec bout de code
    test_user = request.user
    user_to = test_user.following.all()
    to_user = test_user.followed_by.all()
    followed_group = [followed.followed_user for followed in user_to]
    
    if request.method == 'POST':
        # on vérifie ci-dessous si la requête POST nous demande de follow ou d'unfollow un utilisateur
        
        if request.POST.get('user_to_follow', ''):
            user_to_follow_username = request.POST['user_to_follow']
            print(f"USER TO FOLLOW USERNAME EST {user_to_follow_username}")
            # on vérifie ci-dessous que l'utilisateur recherché existe bien
            try:
                # en fait essayer d'englober dans ce bloc try except les blocs if et else juste ne dessous, ça peut marcher
                user_to_follow = User.objects.get(username=user_to_follow_username)
            except:
                user_to_follow=None

            print(f"USER TO FOLLOW EST {user_to_follow}")
            if user_to_follow:
                current_user_id = request.POST['current_user']
                current_user = User.objects.get(id=current_user_id)
                # on vérifie ci-dessous que l'utilisateur n'est pas déjà dans la liste d'abonnements
                if models.UserFollows.objects.filter(user=current_user).filter(followed_user=user_to_follow):
                    # cad si notre utilisateur suit déjà l'utilisateur qu'on veut suivre
                    messages.error(request, "Cet utilisateur est déjà dans votre liste d'abonnements")
                else:
                    print("CHOIX 1")
                    
                    models.UserFollows.objects.create(user=current_user, 
                                                followed_user=user_to_follow)
                    messages.success(request, "L'utilisateur a bien été ajouté à la liste des abonnements")
            
            else:
                print("CHOIX 2")
                messages.error(request, "Aucun utilisateur possédant ce nom n'existe")

        elif request.POST.get('user_to_unfollow', ''):
            print("...LE ELSE EST APPELE DIRECTEMENT...")
            user_to_unfollow_id = request.POST['user_to_unfollow']
            user_to_unfollow = User.objects.get(id=user_to_unfollow_id)
            current_user_id = request.POST['current_user']
            current_user = User.objects.get(id=current_user_id)
            follow_relation = models.UserFollows.objects.filter(user=current_user).filter(followed_user=user_to_unfollow)
            follow_relation.delete()

        else:
            print("CHOIX 3")
            messages.error(request, "Veuillez renseigner un nom d'utilisateur")
        return redirect('subscribers_page')

    return render(request, 'subscribers_page.html', context={'users':users, 'user_to':user_to, 'to_user':to_user,
                                                                'followed_group':followed_group})



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

