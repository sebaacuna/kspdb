from django.contrib import admin
from .models import Game, Craft, PartCollection, Part, Resource, Mu


class RepoAdmin(admin.ModelAdmin):
    list_display = ('repo', 'branch')


class RepoItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)


class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'partName', 'url', 'model_size')
    search_fields = ('name', 'partName')

    def model_size(self, obj):
        if obj.mu:
            return len(obj.mu.bytedata)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MuAdmin(admin.ModelAdmin):
    list_display = ('part_name', 'size')

    def part_name(self, obj):
        return obj.part.name

    def size(self, obj):
        return len(obj.bytedata)

admin.site.register(Game, RepoAdmin)
admin.site.register(Craft, RepoItemAdmin)
admin.site.register(PartCollection, RepoAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Mu, MuAdmin)
