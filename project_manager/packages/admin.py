"""Package admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from .models import PackageRelease
from .models import Package
from .models import PackageImage


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageReleaseAdmin',
    'PackageAdmin',
    'PackageImageAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(PackageRelease)
class PackageReleaseAdmin(admin.ModelAdmin):
    """PackageRelease admin."""

    list_display = (
        'package',
    )
    readonly_fields = (
        'package',
    )
    search_fields = (
        'package__name',
        'package__basename',
        'package__owner__username',
        'package__contributors__username',
    )


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """Package admin."""

    exclude = (
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
    )
    search_fields = (
        'name',
        'basename',
        'owner__username',
        'contributors__username',
    )


@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    """PackageImage admin."""

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
