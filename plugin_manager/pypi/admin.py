# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import PyPiRequirement


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PyPiRequirementAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(PyPiRequirement)
class PyPiRequirementAdmin(admin.ModelAdmin):
    exclude = (
        'slug',
    )
    readonly_fields = (
        'name',
    )
