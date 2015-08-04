from github import GitHub
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Game, Craft, PartCollection, Part
from kspdb.sync import sync_game, sync_parts
from kspdb.parser import CraftParser
from kspdb.mesh import mesh_from_mu


@login_required
def index(request):
    force = bool(request.GET.get('force', False))
    if request.user.game_set.count() == 0:
        return redirect('choose_repo')
    else:
        game = request.user.game_set.first()

    sync_game(game, force)
    try:
        sync_parts(request.user, PartCollection.objects.first(), force)
    except PartCollection.DoesNotExist:
        pass
    social = request.user.social_auth.get(provider='github')
    return render(request, 'index.html', {
        'user_extra': social.extra_data,
        'game': game,
    })


def login(request):
    return render(request, 'login.html')


@login_required
def choose_repo(request):
    repo = request.GET.get('repo')
    branch = request.GET.get('branch')
    if repo and branch:
        game, created = Game.objects.get_or_create(user=request.user)
        game.repo = repo
        game.branch = branch
        game.save()
        return redirect('index')

    social = request.user.social_auth.get(provider='github')
    gh = GitHub(access_token=social.extra_data['access_token'])

    return render(request, 'choose_repo.html', {
        'user_extra': social.extra_data,
        'repositories': gh.user().repos().get(),
    })


@login_required
def craft(request, pk):
    craft = Craft.objects.get(pk=pk)
    parser = CraftParser.model_parser(craft)
    return render(request, 'craft.html', {
        'obj': parser.parse(),
        'parser': parser,
    })


@login_required
def part_mesh(request, pk):
    part = Part.objects.get(pk=pk)
    mesh = mesh_from_mu(part.mu.bytedata)
    return JsonResponse(mesh)
