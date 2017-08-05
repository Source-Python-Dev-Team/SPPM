# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Q

# 3rd-Party Django
from django_filters.filters import BooleanFilter
from django_filters.filterset import FilterSet

from ..models import ForumUser


# =============================================================================
# >> FILTERS
# =============================================================================
class PackageFilter(FilterSet):
    has_contributions = BooleanFilter(method='filter_has_contributions')

    class Meta:
        model = ForumUser

    def filter_has_contributions(self, queryset, name, value):
        value = not value
        return queryset.filter(
            Q(plugins__isnull=value) |
            Q(plugin_contributions__isnull=value) |
            Q(packages__isnull=value) |
            Q(package_contributions__isnull=value) |
            Q(sub_plugins__isnull=value) |
            Q(sub_plugin_contributions__isnull=value)
        )
