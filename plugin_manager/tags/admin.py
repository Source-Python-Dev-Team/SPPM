# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.contrib import admin

# App Imports
from .models import Tag


# =============================================================================
# >> ADMIN CLASSES
# =============================================================================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = (
        'name',
    )
