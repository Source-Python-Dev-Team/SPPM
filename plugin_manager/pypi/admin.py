# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.contrib import admin

# App Imports
from .models import PyPiRequirement


# =============================================================================
# >> ADMIN CLASSES
# =============================================================================
@admin.register(PyPiRequirement)
class PyPiRequirementAdmin(admin.ModelAdmin):
    exclude = (
        'slug',
    )
    readonly_fields = (
        'name',
    )
