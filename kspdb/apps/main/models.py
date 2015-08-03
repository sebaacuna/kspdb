from jsonfield import JSONField
from django.db import models
from django.conf import settings


class Choices(object):
    @classmethod
    def choices(cls):
        return tuple((
            (getattr(cls, attr), attr) for attr in dir(cls)
            if attr not in ['choices', 'name', 'keys']
            and not attr.startswith('_')
        ))

    @classmethod
    def name(cls, target_val):
        for attr in dir(cls):
            if attr not in ['choices', 'name', 'keys'] \
                    and not attr.startswith('_'):
                val = getattr(cls, attr)
                if val == target_val:
                    return str(attr)
        return ''

    @classmethod
    def keys(cls):
        return [c[0] for c in cls.choices()]


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

    @property
    def obj(self):
        from .lib.craft import PartParser
        try:
            return self._obj
        except AttributeError:
            self._obj = PartParser(self.data).parse()
            return self._obj


class Resource(models.Model):
    class FlowMode(Choices):
        NO_FLOW = 'NO_FLOW'
        ALL_VESSEL = 'ALL_VESSEL'
        STACK_PRIORITY_SEARCH = 'STACK_PRIORITY_SEARCH'
        STAGE_PRIORITY_FLOW = 'STAGE_PRIORITY_FLOW'

    name = NameField()
    density = models.FloatField(default=0)
    unitCost = models.FloatField(default=0)
    flowMode = models.CharField(max_length=50, choices=FlowMode.choices())
    transfer = models.CharField(default='NONE', max_length=10)
    hsp = models.IntegerField(default=0)
