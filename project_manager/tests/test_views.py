# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import choice, randint, sample

# Django
from django.test import TestCase
from django.views.generic import TemplateView

# Third Party Django
from rest_framework import status

# App
from project_manager.views import StatisticsView
from test_utils.factories.packages import (
    PackageContributorFactory,
    PackageFactory,
    PackageReleaseFactory,
)
from test_utils.factories.plugins import (
    PluginContributorFactory,
    PluginFactory,
    PluginReleaseFactory,
)
from test_utils.factories.sub_plugins import (
    SubPluginContributorFactory,
    SubPluginFactory,
    SubPluginReleaseFactory,
)
from test_utils.factories.users import ForumUserFactory


# =============================================================================
# TEST CASES
# =============================================================================
class StatisticsViewTestCase(TestCase):

    def test_class_inheritance(self):
        self.assertTrue(
            expr=issubclass(StatisticsView, TemplateView),
        )

    def test_template_name(self):
        self.assertEqual(
            first=StatisticsView.template_name,
            second='statistics.html',
        )

    def test_get_view(self):
        contributing_users = set()
        total_users = randint(20, 30)
        user_list = [ForumUserFactory() for _ in range(total_users)]
        total_download_count = 0

        package_download_count = 0
        package_count = randint(2, 8)
        for _ in range(package_count):
            contributors = sample(user_list, randint(1, 3))
            contributing_users.update(contributors)
            owner = contributors.pop()
            package = PackageFactory(
                owner=owner,
            )
            for contributor in contributors:
                PackageContributorFactory(
                    user=contributor,
                    package=package,
                )
            for _ in range(randint(1, 3)):
                download_count = randint(1, 20)
                package_download_count += download_count
                total_download_count += download_count
                PackageReleaseFactory(
                    package=package,
                    download_count=download_count,
                )

        sub_plugin_download_count = 0
        sub_plugin_count = 0
        plugin_download_count = 0
        plugin_count = randint(4, 8)
        for _ in range(plugin_count):
            contributors = sample(user_list, randint(1, 3))
            contributing_users.update(contributors)
            owner = contributors.pop()
            plugin = PluginFactory(
                owner=owner,
            )
            for contributor in contributors:
                PluginContributorFactory(
                    user=contributor,
                    plugin=plugin,
                )
            for _ in range(randint(1, 3)):
                download_count = randint(1, 20)
                plugin_download_count += download_count
                total_download_count += download_count
                PluginReleaseFactory(
                    plugin=plugin,
                    download_count=download_count,
                )

            if choice([True, False]):
                count = randint(1, 2)
                sub_plugin_count += count
                for _ in range(count):
                    contributors = sample(user_list, randint(1, 3))
                    contributing_users.update(contributors)
                    owner = contributors.pop()
                    sub_plugin = SubPluginFactory(
                        plugin=plugin,
                        owner=owner,
                    )
                    for contributor in contributors:
                        SubPluginContributorFactory(
                            user=contributor,
                            sub_plugin=sub_plugin,
                        )
                    for _ in range(randint(1, 3)):
                        download_count = randint(1, 20)
                        sub_plugin_download_count += download_count
                        total_download_count += download_count
                        SubPluginReleaseFactory(
                            sub_plugin=sub_plugin,
                            download_count=download_count,
                        )

        response = self.client.get('/statistics/')
        self.assertEqual(
            first=response.status_code,
            second=status.HTTP_200_OK,
        )
        data = dict(response.context_data)
        del data['view']
        self.assertDictEqual(
            d1=data,
            d2={
                'users': len(contributing_users),
                'package_count': package_count,
                'plugin_count': plugin_count,
                'sub_plugin_count': sub_plugin_count,
                'total_projects': sum([
                    package_count,
                    plugin_count,
                    sub_plugin_count,
                ]),
                'package_downloads': package_download_count,
                'plugin_downloads': plugin_download_count,
                'sub_plugin_downloads': sub_plugin_download_count,
                'total_downloads': sum([
                    package_download_count,
                    plugin_download_count,
                    sub_plugin_download_count,
                ])
            }
        )