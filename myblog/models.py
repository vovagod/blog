from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    blogger = models.ForeignKey(User, to_field='username', unique=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, default='')
    text = models.TextField(blank=True, default='')
    posts = models.PositiveSmallIntegerField(default=0, null=True)
    subscriptions = models.CharField(max_length=100, blank=True, default='')
    readposts = models.CharField(max_length=100, blank=True, default='')
    time_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('time_created',)

              
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
