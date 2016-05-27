# =============================================================================
# >> IMPORTS
# =============================================================================
# Django Imports
from django.views.generic import ListView

# 3rd-Party Django Imports
from braces.views import OrderableListMixin


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'OrderableListView',
    'OrderablePaginatedListView',
    'PaginatedListView',
)


# =============================================================================
# HELPER CLASSES
# =============================================================================
class PageObject(object):
    def __init__(self, display, url):
        self.display = display
        self.url = url

    def __str__(self):
        return str(self.display)


# =============================================================================
# >> VIEW CLASSES
# =============================================================================
class OrderableListView(OrderableListMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(OrderableListView, self).get_context_data(**kwargs)
        default = self.get_orderable_columns_default()
        order_by = context['order_by']
        order_by_url = (
            'order_by={0}'.format(order_by)
            if order_by in self.get_orderable_columns() and
            order_by != default else None
        )
        ordering_url = (
            'ordering=desc' if context['ordering'] == 'desc' else None
        )
        order_list = filter(None, [order_by_url, ordering_url])
        context.update({
            'order_url': '&'.join(order_list) if order_list else None,
        })
        return context


class PaginatedListView(ListView):
    next_pages = 2
    previous_pages = 2

    def get_next_pages(self):
        if not isinstance(self.next_pages, int) or self.next_pages <= 0:
            raise AttributeError(
                '{0}.next_pages not a valid value ({1}).'.format(
                    self.__class__.__name__,
                    self.next_pages
                )
            )
        return self.next_pages

    def get_previous_pages(self):
        if not isinstance(self.next_pages, int) or self.previous_pages <= 0:
            raise AttributeError(
                '{0}.previous_pages not a valid value ({1}).'.format(
                    self.__class__.__name__,
                    self.previous_pages
                )
            )
        return self.previous_pages

    def get_context_data(self, **kwargs):
        context = super(PaginatedListView, self).get_context_data(**kwargs)
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
        page_url_list = list()
        if context['is_paginated']:
            if current_page != 1:
                page_url_list.append(
                    PageObject('prev', '?page={0}'.format(current_page - 1))
                )
            if 1 not in previous_page_list + [current_page]:
                page_url_list.append(
                    PageObject('1', '?page=1')
                )
            if 2 not in previous_page_list + next_page_list + [current_page]:
                page_url_list.append(
                    PageObject('...', None)
                )
            for item in previous_page_list:
                page_url_list.append(
                    PageObject(item, '?page={0}'.format(item))
                )
            page_url_list.append(
                PageObject(current_page, None)
            )
            for item in next_page_list:
                page_url_list.append(
                    PageObject(item, '?page={0}'.format(item))
                )
            if total_pages - 1 not in (
                    previous_page_list + next_page_list + [current_page]):
                page_url_list.append(
                    PageObject('...', None)
                )
            if total_pages not in next_page_list + [current_page]:
                page_url_list.append(
                    PageObject(total_pages, '?page={0}'.format(total_pages))
                )
            if current_page != total_pages:
                page_url_list.append(
                    PageObject('next', '?page={0}'.format(current_page + 1))
                )
        context.update({
            'page_url_list': page_url_list,
        })
        return context


class OrderablePaginatedListView(OrderableListView, PaginatedListView):
    def get_context_data(self, **kwargs):
        context = super(
            OrderablePaginatedListView, self).get_context_data(**kwargs)
        order_url = context['order_url']
        if order_url:
            for item in context['page_url_list']:
                if item.url is not None:
                    item.url += '&' + order_url
        return context
