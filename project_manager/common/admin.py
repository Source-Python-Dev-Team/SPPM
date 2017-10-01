"""Common admin classes to use for projects."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.contrib import admin


# =============================================================================
# >> ADMINS
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
    list_select_related = (
        'owner__user',
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

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
