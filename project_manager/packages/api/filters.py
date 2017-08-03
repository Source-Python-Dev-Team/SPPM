# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.db.models import Q

# 3rd-Party Django
from django_filters.filters import CharFilter, NumberFilter
from django_filters.filterset import FilterSet

from ..models import Package


# =============================================================================
# >> FILTERS
# =============================================================================
class PackageFilter(FilterSet):
    game = CharFilter(
        'supported_games__basename',
    )
    userid = NumberFilter(method='filter_userid')

    class Meta:
        model = Package
        fields = ('game', )

    def filter_userid(self, queryset, name, value):
        return queryset.filter(
            Q(owner__id=value) | Q(contributors__id=value)
        )
