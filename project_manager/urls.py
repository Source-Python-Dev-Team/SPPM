"""project_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
from .views import StatisticsView
from .packages.views import PackageReleaseDownloadView
from .plugins.views import PluginReleaseDownloadView
from .sub_plugins.views import SubPluginReleaseDownloadView


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
    url(
        # /games/
        regex=r'^games/',
        view=include(
            'project_manager.games.urls',
            namespace='games',
        ),
    ),
    url(
        # /packages/
        regex=r'^packages/',
        view=include(
            'project_manager.packages.urls',
            namespace='packages',
        ),
    ),
    url(
        # /plugins/
        regex=r'^plugins/',
        view=include(
            'project_manager.plugins.urls',
            namespace='plugins',
        ),
    ),
    url(
        # /pypi/
        regex=r'^pypi/',
        view=include(
            'project_manager.pypi.urls',
            namespace='pypi',
        ),
    ),
    url(
        # /tags/
        regex=r'^tags/',
        view=include(
            'project_manager.tags.urls',
            namespace='tags',
        ),
    ),
    url(
        # /users/
        regex=r'^users/',
        view=include(
            'project_manager.users.urls',
            namespace='users',
        ),
    ),
    url(
        # /media/releases/packages/<slug>/<zip_file>
        regex=r'^media/releases/packages/(?P<slug>[\w-]+)/(?P<zip_file>.+)',
        view=PackageReleaseDownloadView.as_view(),
        name='package-download',
    ),
    url(
        # /media/releases/plugins/<slug>/<zip_file>
        regex=r'^media/releases/plugins/(?P<slug>[\w-]+)/(?P<zip_file>.+)',
        view=PluginReleaseDownloadView.as_view(),
        name='plugin-download',
    ),
    url(
        # /media/releases/sub-plugins/<slug>/<sub_plugin_slug>/<zip_file>
        regex=r'^media/releases/sub-plugins/(?P<slug>[\w-]+)/'
              r'(?P<sub_plugin_slug>[\w-]+)/(?P<zip_file>.+)',
        view=SubPluginReleaseDownloadView.as_view(),
        name='sub-plugin-download',
    ),
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
