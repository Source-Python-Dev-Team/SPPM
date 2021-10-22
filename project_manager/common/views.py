"""Common views."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.views.generic import ListView

# Third Party Django
from braces.views import OrderableListMixin


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'OrderableListView',
    'OrderablePaginatedListView',
    'PaginatedListView',
)


# =============================================================================
# HELPERS
# =============================================================================
class _PageObject:
    def __init__(self, display, url):
        self.display = display
        self.url = url

    def __str__(self):
        return str(self.display)


# =============================================================================
# VIEWS
# =============================================================================
class OrderableListView(OrderableListMixin, ListView):
    """View to be inherited for ordering."""

    def get_context_data(self, **kwargs):
        """Update ordering."""
        context = super().get_context_data(**kwargs)
        default = self.get_orderable_columns_default()
        orderable_columns = sorted(self.get_orderable_columns())
        order_by = context['order_by']
        order_by_url = (
            f'order_by={order_by}'
            if order_by in orderable_columns and
            order_by != default else None
        )
        ordering_url = (
            'ordering=desc' if context['ordering'] == 'desc' else None
        )
        order_list = filter(None, [order_by_url, ordering_url])
        context.update({
            'orderable_columns': orderable_columns,
            'order_url': '&'.join(order_list) if order_list else None,
        })
        return context


class PaginatedListView(ListView):
    """View to be inherited for pagination."""

    next_pages = 2
    previous_pages = 2

    def get_next_pages(self):
        """Return the next page URLs."""
        if not isinstance(self.next_pages, int) or self.next_pages <= 0:
            raise AttributeError(
                f'"{self.next_pages}" is not a valid value for '
                f'{self.__class__.__name__}.next_pages.'
            )
        return self.next_pages

    def get_previous_pages(self):
        """Return the previous page URLs."""
        if not isinstance(self.next_pages, int) or self.previous_pages <= 0:
            raise AttributeError(
                f'"{self.next_pages}" is not a valid value for '
                f'{self.__class__.__name__}.previous_pages.'
            )
        return self.previous_pages

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add pagination to the view's context."""
        context = super().get_context_data(object_list=object_list, **kwargs)
        paginator = context['paginator']
        page = context['page_obj']
        total_pages = paginator.num_pages

        previous_pages = self.get_previous_pages()
        next_pages = self.get_next_pages()
        current_page = page.number
        previous_page_list = [x for x in range(
            current_page - previous_pages, current_page) if x > 0]
        next_page_list = [
            x for x in range(
                current_page + 1,
                current_page + 1 + next_pages
            ) if x <= total_pages
        ]
        page_url_list = []
        if context['is_paginated']:
            if current_page != 1:
                page_url_list.append(
                    _PageObject('prev', f'?page={current_page - 1}')
                )
            if 1 not in previous_page_list + [current_page]:
                page_url_list.append(
                    _PageObject('1', '?page=1')
                )
            if 2 not in previous_page_list + next_page_list + [current_page]:
                page_url_list.append(
                    _PageObject('...', None)
                )
            for item in previous_page_list:
                page_url_list.append(
                    _PageObject(item, f'?page={item}')
                )
            page_url_list.append(
                _PageObject(current_page, None)
            )
            for item in next_page_list:
                page_url_list.append(
                    _PageObject(item, f'?page={item}')
                )
            if total_pages - 1 not in (
                    previous_page_list + next_page_list + [current_page]):
                page_url_list.append(
                    _PageObject('...', None)
                )
            if total_pages not in next_page_list + [current_page]:
                page_url_list.append(
                    _PageObject(total_pages, f'?page={total_pages}')
                )
            if current_page != total_pages:
                page_url_list.append(
                    _PageObject('next', f'?page={current_page + 1}')
                )
        context.update({
            'page_url_list': page_url_list,
        })
        return context


class OrderablePaginatedListView(OrderableListView, PaginatedListView):
    """View to be inherited for both ordering and pagination."""

    def get_context_data(self, **kwargs):
        """Update the ordering and pagination."""
        context = super().get_context_data(**kwargs)
        order_url = context['order_url']
        if order_url:
            for item in context['page_url_list']:
                if item.url is not None:
                    item.url += '&' + order_url
        return context
