"""Package admin classes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin

# App
from project_manager.common.admin import ProjectAdmin
from project_manager.packages.admin.inlines import (
    PackageContributorInline,
    PackageGameInline,
    PackageTagInline,
)
from project_manager.packages.models import (
    Package,
    PackageImage,
    PackageRelease,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PackageAdmin',
    'PackageImageAdmin',
    'PackageReleaseAdmin',
)


# =============================================================================
# >> ADMINS
# =============================================================================
@admin.register(Package)
class PackageAdmin(ProjectAdmin):
    """Package admin."""

    inlines = (
        PackageContributorInline,
        PackageGameInline,
        PackageTagInline,
    )


@admin.register(PackageRelease)
class PackageReleaseAdmin(admin.ModelAdmin):
    """PackageRelease admin."""

    actions = None
    fields = (
        'package',
        'version',
        'notes',
        'zip_file',
    )
    list_display = (
        'package',
        'version',
        'notes',
    )
    readonly_fields = (
        'package',
    )
    search_fields = (
        'package__name',
        'package__basename',
        'package__owner__user__username',
        'package__contributors__user__username',
    )
    view_on_site = False


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
