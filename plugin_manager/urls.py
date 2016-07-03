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
from .packages.views import PackageReleaseView
from .plugins.views import PluginReleaseView
from .sub_plugins.views import SubPluginReleaseView


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
urlpatterns = [
    url(
        regex=r'^$',
        view=RedirectView.as_view(
            url='plugins',
            permanent=False,
        ),
        name='index',
    ),
    url(
        regex=r'^statistics',
        view=StatisticsView.as_view(),
    ),
    url(
        regex=r'^admin/',
        view=admin.site.urls,
    ),
    url(
        regex=r'^plugins/',
        view=include(
            'plugin_manager.plugins.urls',
            namespace='plugins',
        ),
    ),
    url(
        regex=r'^packages/',
        view=include(
            'plugin_manager.packages.urls',
            namespace='packages',
        ),
    ),
    url(
        regex=r'^users/',
        view=include(
            'plugin_manager.users.urls',
            namespace='users',
        ),
    ),
    url(
        regex=r'^pypi/',
        view=include(
            'plugin_manager.pypi.urls',
            namespace='pypi',
        ),
    ),
    url(
        regex=r'^games/',
        view=include(
            'plugin_manager.games.urls',
            namespace='games',
        ),
    ),
    url(
        regex=r'^tags/',
        view=include(
            'plugin_manager.tags.urls',
            namespace='tags',
        ),
    ),
    url(
        regex=r'^media/releases/packages/(?P<slug>[\w-]+)/(?P<zip_file>.+)',
        view=PackageReleaseView.as_view(),
        name='plugin-download',
    ),
    url(
        regex=r'^media/releases/plugins/(?P<slug>[\w-]+)/(?P<zip_file>.+)',
        view=PluginReleaseView.as_view(),
        name='plugin-download',
    ),
    url(
        regex=r'^media/releases/sub-plugins/(?P<slug>[\w-]+)/(?P<sub_plugin_slug>[\w-]+)/(?P<zip_file>.+)',
        view=SubPluginReleaseView.as_view(),
        name='sub-plugin-download',
    ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
