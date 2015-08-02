from jsonfield import JSONField
from django.db import models
from django.conf import settings


class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    repo = models.CharField(max_length=100, blank=False)
    branch = models.CharField(max_length=100, blank=False)
    sha = models.CharField(max_length=40, blank=True, null=True)


class Craft(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=255)
    sha = models.CharField(max_length=40, null=True)
    blob = JSONField(null=True)
