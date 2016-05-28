# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.contrib import admin

# App Imports
from .models import OldPackageRelease
from .models import Package
from .models import PackageImage


# =============================================================================
# >> ADMIN CLASSES
# =============================================================================
@admin.register(OldPackageRelease)
class OldPackageReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'package',
        'version',
    )
    readonly_fields = (
        'package',
        'version',
        'version_notes',
        'zip_file',
    )
    search_fields = (
        'package__name',
        'package__basename',
        'package__owner__username',
        'package__contributors__username',
    )


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
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


@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = (
        'package',
        'image',
    )
    readonly_fields = (
        'package',
    )
    search_fields = (
        'package__name',
        'package__basename',
    )
