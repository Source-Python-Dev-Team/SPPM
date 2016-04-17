from django_filters.filterset import FilterSet

from users.models import ForumUser


class ForumUserFilterSet(FilterSet):
    class Meta:
        model = ForumUser
        fields = ['username']
        # order_by = ['username']
