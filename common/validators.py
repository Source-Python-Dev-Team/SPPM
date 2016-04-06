from django.core.validators import RegexValidator


__all__ = (
    'basename_validator',
    'version_validator',
    'sub_plugin_path_validator',
)


basename_validator = RegexValidator(r'^[a-z][0-9a-z_]*[0-9a-z]')
version_validator = RegexValidator(r'^[0-9][0-9a-z.]*[0-9a-z]')
sub_plugin_path_validator = RegexValidator(r'^[a-z][0-9a-z/\\_]*[0-9a-z]')
