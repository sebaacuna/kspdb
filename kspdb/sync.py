import base64
from github import GitHub
import os
from kspdb.apps.main.models import Craft, Part, Mu
from kspdb.parser import PartParser


def sync_game(game, force=False):
    social = game.user.social_auth.get(provider='github')
    gh = GitHub(access_token=social.extra_data['access_token'])
    branch = gh.repos(game.repo).branches().get()[0]
    sha = branch.commit.sha
    if force or sha != game.sha:
        response = gh.repos(game.repo).git().trees(sha).get(
            recursive='1'
        )
        for item in response.tree:
            if item.type == 'blob' and item.path.lower().endswith('.craft'):
                name, _ = os.path.splitext(os.path.basename(item.path))
                craft, created = Craft.objects.get_or_create(
                    game=game, name=name
                )
                if force and craft.url != item.url:
                    blob = gh.repos(game.repo)\
                        .git().blobs(item.sha).get()
                    craft.data = base64.b64decode(blob['content'])\
                        .decode('utf8')
                    craft.url = item.url
                    craft.path = item.path
                    craft.save()
        game.sha = sha
        game.save()


def sync_parts(user, collection, force=False):
    social = user.social_auth.get(provider='github')
    gh = GitHub(access_token=social.extra_data['access_token'])
    branch = gh.repos(collection.repo).branches().get()[0]
    sha = branch.commit.sha
    if force or sha != collection.sha:
        response = gh.repos(collection.repo).git().trees(sha).get(
            recursive='1'
        )
        path_lookup = {}
        for item in response.tree:
            path_lookup[item.path] = item
            if item.type == 'blob' and item.path.lower().endswith('.cfg'):
                name, _ = os.path.splitext(os.path.basename(item.path))
                part, created = Part.objects.get_or_create(
                    collection=collection, name=name
                )
                if force or part.url != item.url:
                    blob = gh.repos(collection.repo)\
                        .git().blobs(item.sha).get()
                    part.data = base64.b64decode(blob['content'])\
                        .decode('utf8')
                    part.url = item.url
                    part.path = item.path
                    obj = PartParser(part.data).parse()
                    part.partName = obj['name']
                    part.save()

        collection.sha = sha
        collection.save()


def sync_mus(user, collection, force=False):
    social = user.social_auth.get(provider='github')
    gh = GitHub(access_token=social.extra_data['access_token'])
    pending_parts = Part.objects.filter(mu__isnull=True)

    if pending_parts.count() == 0:
        return

    branch = gh.repos(collection.repo).branches().get()[0]
    sha = branch.commit.sha
    response = gh.repos(collection.repo).git().trees(sha).get(
        recursive='1'
    )

    path_lookup = {}
    for item in response.tree:
        path_lookup[item.path] = item

    for part in pending_parts:
        try:
            mu_path = '/'.join((
                os.path.dirname(part.path),
                part.obj['mesh']
            ))
        except KeyError:
            print("Mesh not found: ", part.name)
            print(part.obj)
            continue

        try:
            item = path_lookup[mu_path]
        except KeyError:
            print("Path not found: ", mu_path)
            continue

        if item.type == 'blob':
            mu = Mu()
            if force or mu.url != item.url:
                blob = gh.repos(collection.repo)\
                    .git().blobs(item.sha).get()
                mu.bytedata = base64.b64decode(blob['content'])
                mu.url = item.url
                mu.path = item.path
                mu.save()
                part.mu = mu
                part.save()
