from django.conf import settings


def common_urls(request):
    return {
        'FORUM_URL': settings.FORUM_URL,
        'WIKI_URL': settings.WIKI_URL,
        'GITHUB_URL': settings.GITHUB_URL,
    }
