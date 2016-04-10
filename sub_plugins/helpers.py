__all__ = (
    'handle_sub_plugin_upload',
)


def handle_sub_plugin_upload(instance, filename):
    return 'releases/sub_plugins/{0}/{1}/{1}-v{2}.zip'.format(
        instance.plugin.basename,
        instance.basename,
        instance.version,
    )
