from jsonfield import JSONField
from django.db import models
from django.conf import settings


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'max_length': 255,
            'unique': True
        })
        super().__init__(*args, **kwargs)


class Repo(models.Model):
    class Meta:
        abstract = True

    repo = models.CharField(max_length=100, blank=False)
    branch = models.CharField(max_length=100, blank=False)
    sha = models.CharField(max_length=40, blank=True, null=True)


class RepoItem(models.Model):
    class Meta:
        abstract = True

    url = models.URLField(null=True)
    data = models.TextField(null=True)


class Game(Repo):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class Craft(RepoItem):
    game = models.ForeignKey(Game)
    name = NameField()


class Mesh(RepoItem):
    json = JSONField()


class PartCollection(Repo):
    name = NameField()


class Part(RepoItem):
    collection = models.ForeignKey(PartCollection)
    name = NameField()
    partName = models.CharField(max_length=255, null=True)
    mesh = models.OneToOneField(Mesh, null=True)
