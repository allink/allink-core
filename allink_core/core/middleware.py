# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class AllinkUrlRedirectMiddleware:
    """
    This middleware lets you match a specific url and redirect the request to a new url.

    You keep a tuple of url regex pattern/url redirect tuples on your site settings, example:

    URL_REDIRECTS = (
        (r'www\.example\.com/hello/$', 'http://hello.example.com/'),  # noqa
        (r'www\.example2\.com/$', 'http://www.example.com/example2/'),  # noqa
    )
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META['HTTP_HOST'] + request.META['PATH_INFO']
        if hasattr(settings, 'URL_REDIRECTS'):
            for url_pattern, redirect_url in settings.URL_REDIRECTS:
                regex = re.compile(url_pattern)
                if regex.match(host):
                    return HttpResponsePermanentRedirect(redirect_url)
        else:
            return self.get_response(request)
