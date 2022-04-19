from django import forms
from django.contrib.auth.models import User

from . import models

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

RATINGS = [('1','1'), ('2', '2'), ('3','3'), ('4','4'), ('5','5')]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating': forms.RadioSelect(choices=RATINGS),
            'body' : forms.Textarea
            }