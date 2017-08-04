# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.utils import formats

# 3rd-Party Django
from rest_framework.fields import SerializerMethodField
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

# App
from project_manager.games.api.serializers import GameSerializer
from project_manager.packages.api.serializers.common import (
    PackageRequirementSerializer
)
from project_manager.requirements.api.serializers import (
    DownloadRequirementSerializer,
    PyPiRequirementSerializer,
    VersionControlRequirementSerializer,
)
from project_manager.tags.api.serializers import TagSerializer
from project_manager.users.api.serializers import ForumUserSerializer


# =============================================================================
# >> MIXINS
# =============================================================================
class ProjectSerializer(ModelSerializer):
    current_release = SerializerMethodField()
    owner = ForumUserSerializer(
        read_only=True,
    )
    contributors = ForumUserSerializer(
        many=True,
        read_only=True,
    )
    created = SerializerMethodField()
    updated = SerializerMethodField()
    package_requirements = PackageRequirementSerializer(
        many=True,
        read_only=True,
    )
    download_requirements = DownloadRequirementSerializer(
        many=True,
        read_only=True,
    )
    pypi_requirements = PyPiRequirementSerializer(
        many=True,
        read_only=True,
    )
    vcs_requirements = VersionControlRequirementSerializer(
        many=True,
        read_only=True,
    )
    supported_games = GameSerializer(
        many=True,
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        fields = (
            'name',
            'slug',
            'total_downloads',
            'current_release',
            'created',
            'updated',
            'synopsis',
            'description',
            'configuration',
            'logo',
            'owner',
            'contributors',
            'package_requirements',
            'download_requirements',
            'pypi_requirements',
            'vcs_requirements',
            'supported_games',
            'tags',
        )
        read_only_fields = (
            'slug',
        )

    @property
    def reverse_path(self):
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement "reverse_path".'
        )

    @staticmethod
    def get_download_kwargs(obj, release):
        return {
            'slug': obj.slug,
            'zip_file': release.file_name,
        }

    def get_current_release(self, obj):
        try:
            release = obj.releases.all()[0]
        except IndexError:
            return {}
        zip_url = reverse(
            viewname=f'{self.reverse_path}-download',
            kwargs=self.get_download_kwargs(
                obj=obj,
                release=release,
            ),
            request=self.context['request']
        )
        return {
            'version': release.version,
            'notes': str(release.notes) if release.notes else release.notes,
            'zip_file': zip_url,
        }

    def get_created(self, obj):
        return self.get_date_time_dict(timestamp=obj.created)

    def get_updated(self, obj):
        try:
            release = obj.releases.all()[0]
        except IndexError:
            return self.get_date_time_dict(timestamp=obj.created)
        return self.get_date_time_dict(timestamp=release.modified)

    def get_date_time_dict(self, timestamp):
        return {
            'actual': timestamp,
            'locale': self.get_date_display(
                date=timestamp,
                date_format='DATE_FORMAT',
            ),
            'locale_short': self.get_date_display(
                date=timestamp,
                date_format='SHORT_DATE_FORMAT',
            )
        }

    @staticmethod
    def get_date_display(date, date_format):
        return formats.date_format(
            value=date,
            format=date_format,
        ) if date else date
