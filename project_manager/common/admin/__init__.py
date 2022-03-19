"""Common admin classes to use for projects."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib import admin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'ProjectAdmin',
    'ProjectReleaseAdmin',
)


# =============================================================================
# ADMINS
# =============================================================================
class ProjectAdmin(admin.ModelAdmin):
    """Base admin class for projects."""

    actions = None
    fieldsets = (
        (
            'Project Info',
            {
                'classes': ('wide',),
                'fields': (
                    'name',
                    'owner',
                    'configuration',
                    'description',
                    'synopsis',
                    'logo',
                    'topic',
                ),
            }
        ),
        (
            'Metadata',
            {
                'classes': ('collapse',),
                'fields': (
                    'basename',
                    'slug',
                    'created',
                    'updated',
                ),
            },
        )
    )
    list_display = (
        'name',
        'basename',
        'owner',
    )
    raw_id_fields = (
        'owner',
    )
    readonly_fields = (
        'basename',
        'created',
        'slug',
        'updated',
    )
    search_fields = (
        'name',
        'basename',
        'owner__user__username',
        'contributors__user__username',
    )

    def has_add_permission(self, request):
        """Disallow creation of a Project in the Admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deletion of Project in the Admin."""
        return False


class ProjectReleaseAdmin(admin.ModelAdmin):
    """Base admin class for project releases."""

    fieldsets = (
        (
            'Release Info',
            {
                'classes': ('wide',),
                'fields': (
                    'version',
                    'notes',
                    'zip_file',
                ),
            }
        ),
        (
            'Metadata',
            {
                'classes': ('collapse',),
                'fields': (
                    'created',
                    'created_by',
                    'download_count',
                ),
            },
        )
    )
    list_display = (
        'version',
        'created',
    )
    readonly_fields = (
        'zip_file',
        'download_count',
        'created',
        'created_by',
    )
    search_fields = (
        'version',
    )
    view_on_site = False

    def has_add_permission(self, request):
        """Disallow creation of a Project in the Admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deletion of Project in the Admin."""
        return False
