"""plugin_manager URL Configuration

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
        # http://plugins.sourcepython.com/
        regex=r'^$',
        view=RedirectView.as_view(
            url='plugins',
            permanent=False,
        ),
        name='index',
    ),
    url(
        # http://plugins.sourcepython.com/statistics/
        regex=r'^statistics',
        view=StatisticsView.as_view(),
        name='statistics',
    ),
    url(
        # http://plugins.sourcepython.com/admin/
        regex=r'^admin/',
        view=admin.site.urls,
    ),
    url(
        # http://plugins.sourcepython.com/games/
        regex=r'^games/',
        view=include(
            'plugin_manager.games.urls',
            namespace='games',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/packages/
        regex=r'^packages/',
        view=include(
            'plugin_manager.packages.urls',
            namespace='packages',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/plugins/
        regex=r'^plugins/',
        view=include(
            'plugin_manager.plugins.urls',
            namespace='plugins',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/pypi/
        regex=r'^pypi/',
        view=include(
            'plugin_manager.pypi.urls',
            namespace='pypi',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/tags/
        regex=r'^tags/',
        view=include(
            'plugin_manager.tags.urls',
            namespace='tags',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/users/
        regex=r'^users/',
        view=include(
            'plugin_manager.users.urls',
            namespace='users',
        ),
    ),
    url(
        # http://plugins.sourcepython.com/media/releases/packages/<slug>/<zip_file>
        regex=r'^media/releases/packages/(?P<slug>[\w-]+)/(?P<zip_file>.+)',
        view=PackageReleaseDownloadView.as_view(),
        name='package-download',
    ),
    url(
        # http://plugins.sourcepython.com/media/releases/plugins/<slug>/<zip_file>
        regex=r'^media/releases/plugins/(?P<slug>[\w-]+)/(?P<zip_file>.+)',
        view=PluginReleaseDownloadView.as_view(),
        name='plugin-download',
    ),
    url(
        # http://plugins.sourcepython.com/media/releases/sub-plugins/<slug>/<sub_plugin_slug>/<zip_file>
        regex=r'^media/releases/sub-plugins/(?P<slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)/(?P<zip_file>.+)',
        view=SubPluginReleaseDownloadView.as_view(),
        name='sub-plugin-download',
    ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
