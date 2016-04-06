def handle_plugin_upload(instance, filename):
    return 'releases/plugins/{0}/{1}/{2}'.format(
        instance.basename, instance.version, filename)
