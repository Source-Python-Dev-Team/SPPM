"""Common helper functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from zipfile import ZipFile, BadZipfile

# 3rd-Party Python
from configobj import ConfigObj

# Django
from django.conf import settings
from django.core.exceptions import ValidationError

# App
from project_manager.requirements.models import (
    DownloadRequirement,
    PyPiRequirement,
    VersionControlRequirement,
)


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'add_download_requirement',
    'add_package_requirement',
    'add_pypi_requirement',
    'add_vcs_requirement',
    'find_image_number',
    'flush_requirements',
    'get_file_list',
    'get_groups',
    'get_requirements',
    'handle_project_image_upload',
    'handle_project_logo_upload',
    'handle_release_zip_file_upload',
    'reset_requirements',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def find_image_number(directory, slug):
    """Return the next available image number."""
    path = settings.MEDIA_ROOT / 'images' / directory / slug
    current_files = [x.namebase for x in path.files()] if path.isdir() else []
    return '%04d' % (max(map(int, current_files or [0])) + 1)


def get_groups(iterable, count=3):
    """Return lists from the given iterable in chunks of 'count'."""
    if not iterable:
        return iterable
    iterable = list(iterable)
    remainder = len(iterable) % count
    iterable.extend([''] * (count - remainder))
    return zip(*(iter(iterable),) * count)


def get_requirements(zip_file, requirement_path):
    """Return the requirements for the release."""
    for zipped_file in zip_file.filelist:
        if zipped_file.filename != requirement_path:
            continue
        ini = zip_file.open(zipped_file)
        return ConfigObj(ini)
    return {}


def handle_project_image_upload(instance, filename):
    """Handle uploading the image by directing to the proper directory."""
    return instance.handle_image_upload(filename)


def handle_project_logo_upload(instance, filename):
    """Handle uploading the logo by directing to the proper directory."""
    return instance.handle_logo_upload(instance, filename)


def handle_release_zip_file_upload(instance, filename):
    """Handle uploading the zip file by directing to the proper directory."""
    return instance.handle_zip_file_upload(filename)


def add_package_requirement(package_basename, project):
    """Add a Package requirement to a project."""
    from project_manager.packages.models import Package
    try:
        package = Package.objects.get(basename=package_basename)
    except Package.DoesNotExist:
        return False
    project.package_requirements.add(package)
    return True


def add_pypi_requirement(package_basename, project):
    """Add a PyPi requirement to a project."""
    package, created = PyPiRequirement.objects.get_or_create(
        name=package_basename,
    )
    project.pypi_requirements.add(package)


def add_vcs_requirement(name, url, project):
    """Add a VCS requirement to a project."""
    package, created = VersionControlRequirement.objects.get_or_create(
        name=name,
        url=url,
    )
    project.vcs_requirements.add(package)


def add_download_requirement(name, url, desc, project):
    """Add a Download requirement to a project."""
    package, created = DownloadRequirement.objects.get_or_create(
        name=name,
        url=url,
        description=desc,
    )
    project.download_requirements.add(package)


def reset_requirements(project):
    """Clear all requirements for the given project."""
    project.package_requirements.clear()
    project.pypi_requirements.clear()
    project.vcs_requirements.clear()
    project.download_requirements.clear()


def flush_requirements():
    """Remove any requirements that no longer are required by any projects."""
    PyPiRequirement.objects.filter(
        required_in_packages__isnull=True,
        required_in_plugins__isnull=True,
        required_in_subplugins__isnull=True,
    ).delete()
    VersionControlRequirement.objects.filter(
        packages__isnull=True,
        plugins__isnull=True,
        sub_plugins__isnull=True,
    ).delete()
    DownloadRequirement.objects.filter(
        packages__isnull=True,
        plugins__isnull=True,
        sub_plugins__isnull=True,
    ).delete()


def get_file_list(zip_file):
    try:
        return [
            x for x in ZipFile(zip_file).namelist() if not x.endswith('/')
        ]
    except BadZipfile:
        raise ValidationError({
            'zip_file': 'Given file is not a valid zip file.'
        })
