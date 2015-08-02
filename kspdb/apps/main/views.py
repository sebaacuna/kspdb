from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from github import GitHub
from .models import Game


@login_required
def index(request):
    if request.user.game_set.count() == 0:
        return redirect('choose_repo')
    else:
        game = request.user.game_set.first()

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
    if repo:
        game, created = Game.objects.get_or_create(user=request.user)
        game.repo = repo
        game.save()
        return redirect('index')

    social = request.user.social_auth.get(provider='github')
    gh = GitHub(access_token=social.extra_data['access_token'])

    return render(request, 'choose_repo.html', {
        'user_extra': social.extra_data,
        'repositories': gh.user().repos().get(),
    })
