def handle_package_upload(instance, filename):
    return 'releases/packages/{0}/{1}/{2}'.format(
        instance.basename, instance.version, filename)
