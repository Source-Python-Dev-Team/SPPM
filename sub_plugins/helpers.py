def handle_sub_plugin_upload(instance, filename):
    return 'releases/sub_plugins/{0}/{1}/{2}/{3}'.format(
        instance.plugin.basename,
        instance.basename,
        instance.version,
        filename
    )
