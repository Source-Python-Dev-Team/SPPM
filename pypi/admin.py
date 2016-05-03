from django.contrib import admin

from .models import PyPiRequirement


@admin.register(PyPiRequirement)
class PyPiRequirementAdmin(admin.ModelAdmin):
    exclude = (
        'slug',
    )
    readonly_fields = (
        'name',
    )
