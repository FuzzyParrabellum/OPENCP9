from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageField

from PIL import Image

class Ticket(models.Model):

    IMG_MAX_SIZE = (200,200)

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def resize_img(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMG_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_img()


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(\
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note")
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.CharField(max_length=8192, blank=True, verbose_name="Commentaire")
    user = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    # Your UserFollows model definition goes here

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )

    user = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,\
        related_name='following')

    followed_user = models.ForeignKey(\
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,\
        related_name='followed_by')