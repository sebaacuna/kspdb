from django.conf.urls import patterns, url, include
from django.contrib import admin
from kspdb.apps.main import views

urlpatterns = patterns(
    '',
    url('^$', views.index, name="index"),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('^login/$', views.login, name="login"),

    url('^choose_repo$', views.choose_repo, name='choose_repo'),

    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
