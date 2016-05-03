from django.contrib import admin

from .models import SubPlugin


@admin.register(SubPlugin)
class SubPluginAdmin(admin.ModelAdmin):
    exclude = (
        'zip_file',
        'version',
        'slug',
    )
    list_display = (
        'name',
        'basename',
        'owner',
    )
    list_select_related = (
        'owner',
    )
    raw_id_fields = (
        'owner',
    )
    readonly_fields = (
        'basename',
        'current_version',
        'date_created',
        'date_last_updated',
    )
    search_fields = (
        'name',
        'basename',
        'owner__username',
        'contributors__username',
    )
