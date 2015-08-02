def save_data(backend, user, response, *args, **kwargs):
    if backend.name == 'github':
        social = user.social_auth.get(provider='github')
        social.extra_data.update({
            'avatar_url': response['avatar_url'],
        })
        social.save()
