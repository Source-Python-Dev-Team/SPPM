from django.contrib import admin
from django.test import TestCase

from games.admin import GameAdmin


class GameTestCase(TestCase):
    def test_model_inheritance(self):
        self.assertTrue(
            expr=issubclass(GameAdmin, admin.ModelAdmin),
        )

    def test_exclude(self):
        self.assertTupleEqual(
            tuple1=GameAdmin.exclude,
            tuple2=('slug',),
        )

    def test_list_display(self):
        self.assertTupleEqual(
            tuple1=GameAdmin.list_display,
            tuple2=(
                'basename',
                'name',
                'icon',
            ),
        )

    def test_list_editable(self):
        self.assertTupleEqual(
            tuple1=GameAdmin.list_editable,
            tuple2=(
                'name',
                'icon',
            ),
        )

    def test_readonly_fields(self):
        self.assertTupleEqual(
            tuple1=GameAdmin.readonly_fields,
            tuple2=('basename',),
        )

    def test_search_fields(self):
        self.assertTupleEqual(
            tuple1=GameAdmin.search_fields,
            tuple2=(
                'name',
                'basename',
            ),
        )
