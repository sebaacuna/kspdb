import base64
from github import GitHub
import os
from kspdb.apps.main.models import Craft, Part
from kspdb.parser import PartParser


def sync_game(game):
    social = game.user.social_auth.get(provider='github')
    gh = GitHub(access_token=social.extra_data['access_token'])
    branch = gh.repos(game.repo).branches().get()[0]
    sha = branch.commit.sha
    if sha != game.sha:
        response = gh.repos(game.repo).git().trees(sha).get(
            recursive='1'
        )
        for item in response.tree:
            if item.type == 'blob' and \
               item.path.lower().endswith('.craft'):
                name, _ = os.path.splitext(os.path.basename(item.path))
                craft, created = Craft.objects.get_or_create(
                    game=game, name=name
                )
                if craft.url != item.url:
                    blob = gh.repos(game.repo)\
                        .git().blobs(item.sha).get()
                    craft.data = base64.b64decode(blob['content'])\
                        .decode('utf8')
                    craft.url = item.url
                    craft.save()
        game.sha = sha
        game.save()


def sync_parts(user, collection):
    social = user.social_auth.get(provider='github')
    gh = GitHub(access_token=social.extra_data['access_token'])
    branch = gh.repos(collection.repo).branches().get()[0]
    sha = branch.commit.sha
    if sha != collection.sha:
        response = gh.repos(collection.repo).git().trees(sha).get(
            recursive='1'
        )
        for item in response.tree:
            if item.type == 'blob' and \
               item.path.lower().endswith('.cfg'):
                name, _ = os.path.splitext(os.path.basename(item.path))
                part, created = Part.objects.get_or_create(
                    collection=collection, name=name
                )
                if part.url != item.url:
                    blob = gh.repos(collection.repo)\
                        .git().blobs(item.sha).get()
                    part.data = base64.b64decode(blob['content'])\
                        .decode('utf8')
                    part.url = item.url
                    obj = PartParser(part.data).parse()
                    part.partName = obj['name']
                    part.save()
        collection.sha = sha
        collection.save()
