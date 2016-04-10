__all__ = (
    'handle_package_upload',
)


def handle_package_upload(instance, filename):
    return 'releases/packages/{0}/{0}-v{1}.zip'.format(
        instance.basename,
        instance.version
    )
