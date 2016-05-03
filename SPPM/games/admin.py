from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    exclude = (
        'slug',
    )
    list_display = (
        'name',
        'basename',
    )
    search_fields = (
        'name',
        'basename',
    )
