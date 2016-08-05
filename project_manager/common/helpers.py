# =============================================================================
# >> IMPORTS
# =============================================================================
# 3rd-Party Python
from configobj import ConfigObj

# Django
from django.conf import settings

# App
from project_manager.pypi.models import PyPiRequirement
from .models import DownloadRequirement, VersionControlRequirement


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
    'get_groups',
    'get_requirements',
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
    if not iterable:
        return iterable
    iterable = list(iterable)
    remainder = len(iterable) % count
    iterable.extend([''] * (count - remainder))
    return zip(*(iter(iterable), ) * count)


def get_requirements(zip_file, requirement_path):
    for zipped_file in zip_file.filelist:
        if zipped_file.filename == requirement_path:
            break
    else:
        return {}
    ini = zip_file.open(zipped_file)
    return ConfigObj(ini)


def add_package_requirement(package_basename, project):
    from project_manager.packages.models import Package
    try:
        package = Package.objects.get(basename=package_basename)
    except Package.DoesNotExist:
        return False
    project.package_requirements.add(package)
    return True


def add_pypi_requirement(package_basename, project):
    package, created = PyPiRequirement.objects.get_or_create(name=package_basename)
    project.pypi_requirements.add(package)


def add_vcs_requirement(name, url, project):
    package, created = VersionControlRequirement.objects.get_or_create(
        name=name,
        url=url,
    )
    project.vcs_requirements.add(package)


def add_download_requirement(name, url, desc, project):
    package, created = DownloadRequirement.objects.get_or_create(
        name=name,
        url=url,
        description=desc,
    )
    project.download_requirements.add(package)


def reset_requirements(project):
    project.package_requirements.clear()
    project.pypi_requirements.clear()
    project.vcs_requirements.clear()
    project.download_requirements.clear()


def flush_requirements():
    PyPiRequirement.objects.filter(
        required_in_packages__isnull=True,
        required_in_plugins__isnull=True,
        required_in_sub_plugins__isnull=True,
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
