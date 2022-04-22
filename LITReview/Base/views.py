from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from itertools import chain
from django.db.models import CharField, Value

from . import models, forms


@login_required
def HomePage(request):
    # le code ci-dessous devrait afficher tous les tickets de l'utilisateur actuel
    # il faudrait également pouvoir afficher ses reviews et les tickets et reviews
    # des utilisateurs qu'il suit

    current_user = request.user

    subscribed_tickets = models.Ticket.objects.filter(user__followed_by__user=current_user)
    subscribed_tickets = subscribed_tickets.annotate(content_type=Value('TICKET', CharField()))
    current_user_tickets = models.Ticket.objects.filter(user=current_user)
    current_user_tickets = current_user_tickets.annotate(content_type=Value('TICKET', CharField()))
    tickets = subscribed_tickets.union(current_user_tickets)
    q = tickets
    for ticket in tickets:
        if models.Review.objects.filter(ticket=ticket):
            print(f"Il  a bien une review au ticket n°{ticket.id}")
            reviews = models.Review.objects.filter(ticket=ticket)
            reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
            q = chain(q, reviews)
    posts = sorted(
        q,
        key= lambda post: post.time_created,
        reverse=True
    )
    # q.order_by('time_created')
    
    return render(request,
        'account/HomePage.html', context={'posts': posts, 'section': 'HomePage'})

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
def review_upload(request, ticket_id):
    form = forms.ReviewForm()
    ticket = models.Ticket.objects.get(id=ticket_id)
    print(f'THE TICKET ID {ticket.id}')
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('HomePage')
    return render(request, 'critics/review_creation.html', context={'form': form,
                                                                    'ticket': ticket})


@login_required
def review_and_ticket_upload(request):
    review_form = forms.ReviewForm
    ticket_form = forms.TicketForm
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if review_form.is_valid() and ticket_form.is_valid():
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
            # on vérifie ci-dessous que l'utilisateur recherché existe bien
            try:
                # en fait essayer d'englober dans ce bloc try except les blocs if et else juste ne dessous, ça peut marcher
                user_to_follow = User.objects.get(username=user_to_follow_username)
            except:
                user_to_follow=None

            if user_to_follow:
                current_user_id = request.POST['current_user']
                current_user = User.objects.get(id=current_user_id)
                # on vérifie ci-dessous que l'utilisateur n'est pas déjà dans la liste d'abonnements
                if models.UserFollows.objects.filter(user=current_user).filter(followed_user=user_to_follow):
                    # cad si notre utilisateur suit déjà l'utilisateur qu'on veut suivre
                    messages.error(request, "Cet utilisateur est déjà dans votre liste d'abonnements")
                else:                    
                    models.UserFollows.objects.create(user=current_user, 
                                                followed_user=user_to_follow)
                    messages.success(request, "L'utilisateur a bien été ajouté à la liste des abonnements")
            
            else:
                messages.error(request, "Aucun utilisateur possédant ce nom n'existe")

        elif request.POST.get('us</div>er_to_unfollow', ''):
            user_to_unfollow_id = request.POST['user_to_unfollow']
            user_to_unfollow = User.objects.get(id=user_to_unfollow_id)
            current_user_id = request.POST['current_user']
            current_user = User.objects.get(id=current_user_id)
            follow_relation = models.UserFollows.objects.filter(user=current_user).filter(followed_user=user_to_unfollow)
            follow_relation.delete()

        else:
            messages.error(request, "Veuillez renseigner un nom d'utilisateur")
        return redirect('subscribers_page')

    return render(request, 'subscribers_page.html', context={'users':users, 'user_to':user_to, 'to_user':to_user,
                                                                'followed_group':followed_group})

@login_required
def own_posts(request):
    # code tiré de la view de HomePage
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = models.Review.objects.filter(user=current_user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = chain(tickets, reviews)
    
    posts = sorted(
        posts,
        key= lambda post: post.time_created,
        reverse=True
    )

    if request.method == 'POST':
        try :
            ticket_id = request.POST['current_ticket_id']
            # ici la logique pour modifier un ticket
            if request.POST.get('ticket_to_remove', ''):
            # là la logique pour supprimer un ticket
                ticket_to_remove = models.Ticket.objects.get(id=ticket_id)
                ticket_to_remove.delete()
                messages.success(request, 
                "Le ticket a bien été supprimé de la base de données.")
                return redirect("own_posts")
                
            # if request.POST.get('ticket_to_modify', ''):
            #     print("IL Y A BIEN UN TICKET TO MODIFY")
            #     ticket_to_modify = models.Ticket.objects.get(id=ticket_id)
            #     print(f"LE TICKET A MODIFY A POUR ID {ticket_id}")
            #     return redirect("own_posts")

        except :
            review_id = request.POST['current_review_id']
            print(f"REVIEW ID EST BIEN DE {review_id}")
            if request.POST.get('review_to_remove', ''):
            # là la logique pour supprimer un ticket
                review_to_remove = models.Review.objects.get(id=review_id)
                review_to_remove.delete()
                messages.success(request, 
                "La review a bien été supprimé de la base de données.")
                return redirect("own_posts")
            # if request.POST.get('review_to_modify', ''):
            #     review_to_modify = models.Review.objects.get(id=review_id)
                
            #     return render(request, 'review_modification.html', \
            #         context={'review_id': review_id})
        return redirect("own_posts")
    return render(request, 'own_posts.html', context={'posts': posts,\
                                                        'section': 'Posts'})

@login_required
def ticket_modification(request, ticket_id):
    ticket_to_modify = models.Ticket.objects.get(id=ticket_id)
    
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, \
            instance=ticket_to_modify)
        if form.is_valid():
            form.save()
            return redirect('own_posts')

    else:
        form = forms.TicketForm(instance=ticket_to_modify)

    return render(request, 'critics/ticket_creation.html', context={'form': form})

@login_required
def review_modification(request, review_id):
    review_to_modify = models.Review.objects.get(id=review_id)
    ticket = review_to_modify.ticket
    
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review_to_modify)
        if form.is_valid():
            form.save()
            return redirect('own_posts')

    else:
        form = forms.ReviewForm(instance=review_to_modify)

    return render(request, 'critics/review_modification.html', \
        context={'form':form, 'ticket': ticket})