# =============================================================================
# IMPORTS
# =============================================================================
# Python
from random import randint
from unittest import mock

# Django
from django.test import TestCase

# App
from project_manager.sub_plugins.constants import (
    SUB_PLUGIN_IMAGE_URL,
    SUB_PLUGIN_LOGO_URL,
    SUB_PLUGIN_RELEASE_URL,
)
from project_manager.sub_plugins.helpers import (
    handle_sub_plugin_image_upload,
    handle_sub_plugin_logo_upload,
    handle_sub_plugin_zip_upload,
)
from test_utils.factories.sub_plugins import (
    SubPluginFactory,
    SubPluginImageFactory,
    SubPluginReleaseFactory,
)


# =============================================================================
# TEST CASES
# =============================================================================
class SubPluginZipFileTestCase(TestCase):
    # TODO: Add tests for SubPluginZipFile class
    pass


class HelperFunctionsTestCase(TestCase):
    def test_handle_sub_plugin_zip_upload(self):
        obj = SubPluginReleaseFactory()
        plugin_slug = obj.sub_plugin.plugin.slug
        slug = obj.sub_plugin.slug
        self.assertEqual(
            first=handle_sub_plugin_zip_upload(obj),
            second=(
                f'{SUB_PLUGIN_RELEASE_URL}{plugin_slug}/{slug}/'
                f'{slug}-v{obj.version}.zip'
            ),
        )

    def test_handle_sub_plugin_logo_upload(self):
        obj = SubPluginFactory()
        plugin_slug = obj.plugin.slug
        extension = 'jpg'
        filename = f'test_image.{extension}'
        self.assertEqual(
            first=handle_sub_plugin_logo_upload(
                instance=obj,
                filename=filename,
            ),
            second=(
                f'{SUB_PLUGIN_LOGO_URL}{plugin_slug}/{obj.slug}.{extension}'
            ),
        )

    def test_handle_sub_plugin_image_upload(self):
        obj = SubPluginImageFactory()
        plugin_slug = obj.sub_plugin.plugin.slug
        slug = obj.sub_plugin.slug
        extension = 'jpg'
        filename = f'test_image.{extension}'
        image_number = f'{randint(1, 10):04}'
        with mock.patch(
            target='project_manager.sub_plugins.helpers.find_image_number',
            return_value=image_number,
        ):
            self.assertEqual(
                first=handle_sub_plugin_image_upload(
                    instance=obj,
                    filename=filename,
                ),
                second=(
                    f'{SUB_PLUGIN_IMAGE_URL}{plugin_slug}/{slug}/'
                    f'{image_number}.{extension}'
                ),
            )
