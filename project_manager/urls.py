"""Base App URLs."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

# App
from project_manager.views import StatisticsView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        # /
        regex=r'^$',
        view=RedirectView.as_view(
            url='plugins',
            permanent=False,
        ),
        name='index',
    ),
    url(
        # /statistics/
        regex=r'^statistics/',
        view=StatisticsView.as_view(),
        name='statistics',
    ),
    url(
        # /admin/
        regex=r'^admin/',
        view=admin.site.urls,
    ),
    url(
        regex=r'^api/',
        view=include(
            'project_manager.api.urls',
            namespace='api',
        ),
        name='api',
    ),
    # url(
    #     regex=r'^plugins/',
    #     view=,
    #     name='plugins',
    # ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
