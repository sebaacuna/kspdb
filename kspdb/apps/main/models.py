from django.db import models
from django.conf import settings


class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    repo = models.CharField(max_length=100)
