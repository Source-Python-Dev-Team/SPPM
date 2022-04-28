"""Base App URLs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

# App
from project_manager.views import StatisticsView
from project_manager.packages.views import PackageReleaseDownloadView
from project_manager.plugins.views import PluginReleaseDownloadView
from project_manager.sub_plugins.views import SubPluginReleaseDownloadView


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    path(
        # /
        route='',
        view=RedirectView.as_view(
            url='plugins',
            permanent=False,
        ),
        name='index',
    ),
    path(
        # /statistics/
        route='statistics/',
        view=StatisticsView.as_view(),
        name='statistics',
    ),
    path(
        # /admin/
        route='admin/',
        view=admin.site.urls,
    ),
    path(
        route='api/',
        view=include(
            'project_manager.api.urls',
            namespace='api',
        ),
        name='api',
    ),
    path(
        route='packages/',
        view=include(
            'project_manager.packages.urls',
            namespace='packages',
        ),
        name='packages',
    ),
    path(
        route='plugins/',
        view=include(
            'project_manager.plugins.urls',
            namespace='plugins',
        ),
        name='plugins',
    ),
    path(
        # /media/releases/packages/<slug>/<zip_file>
        route='media/releases/packages/<slug:slug>/<str:zip_file>',
        view=PackageReleaseDownloadView.as_view(),
        name='package-download',
    ),
    path(
        # /media/releases/plugins/<slug>/<zip_file>
        route='media/releases/plugins/<slug:slug>/<str:zip_file>',
        view=PluginReleaseDownloadView.as_view(),
        name='plugin-download',
    ),
    path(
        # /media/releases/sub-plugins/<slug>/<sub_plugin_slug>/<zip_file>
        route=(
            'media/releases/sub-plugins/<slug:slug>/<slug:sub_plugin_slug>/'
            '<str:zip_file>'
        ),
        view=SubPluginReleaseDownloadView.as_view(),
        name='sub-plugin-download',
    ),
    path(
        route='users/',
        view=include(
            'users.urls',
            namespace='users',
        ),
        name='users',
    ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

if settings.DEBUG:  # pragma: no branch
    import debug_toolbar
    urlpatterns += [
        path(
            route='__debug__/',
            view=include(debug_toolbar.urls),
        ),
    ]

if settings.LOCAL:  # pragma: no branch
    urlpatterns += [
        path(
            route='accounts/',
            view=include('django.contrib.auth.urls'),
        )
    ]
