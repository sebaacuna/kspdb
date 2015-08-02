from django.contrib import admin
from .models import Game, Craft, PartCollection, Part


class RepoAdmin(admin.ModelAdmin):
    list_display = ('repo', 'branch')


class RepoItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)


class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'partName', 'url')
    search_fields = ('name', 'partName')


admin.site.register(Game, RepoAdmin)
admin.site.register(Craft, RepoItemAdmin)
admin.site.register(PartCollection, RepoAdmin)
admin.site.register(Part, PartAdmin)
