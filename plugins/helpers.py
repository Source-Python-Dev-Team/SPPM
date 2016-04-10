__all__ = (
    'handle_plugin_upload',
)


def handle_plugin_upload(instance, filename):
    return 'releases/plugins/{0}/{0}-v{1}.zip'.format(
        instance.basename,
        instance.version,
    )
