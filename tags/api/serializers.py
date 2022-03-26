"""Tag serializers for APIs."""

# =============================================================================
# IMPORTS
# =============================================================================
# Third Party Django
from rest_framework.fields import IntegerField
from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer

# App
from tags.models import Tag


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'RelatedTagSerializer',
    'TagListSerializer',
    'TagRetrieveSerializer',
)


# =============================================================================
# SERIALIZERS
# =============================================================================
class RelatedTagSerializer(RelatedField):
    """Serializer for project tag fields."""

    def to_representation(self, value):
        """Return the name of the project."""
        # TODO: return the url once the paths exist
        # return {'name': value.name, 'id': value.pk, 'url': value.get_absolute_url()}
        return {'name': value.name, 'id': value.pk}


class TagRetrieveSerializer(ModelSerializer):
    """Serializer for project Tags on retrieve."""

    packages = RelatedTagSerializer(many=True, read_only=True)
    plugins = RelatedTagSerializer(many=True, read_only=True)
    subplugins = RelatedTagSerializer(many=True, read_only=True)

    class Meta:
        """Define metaclass attributes."""

        model = Tag
        fields = (
            'name',
            'packages',
            'plugins',
            'subplugins',
        )


class TagListSerializer(ModelSerializer):
    """Serializer for project Tags on list."""

    package_count = IntegerField()
    plugin_count = IntegerField()
    subplugin_count = IntegerField()
    project_count = IntegerField()

    class Meta:
        """Define metaclass attributes."""

        model = Tag
        fields = (
            'name',
            'package_count',
            'plugin_count',
            'subplugin_count',
            'project_count',
        )
