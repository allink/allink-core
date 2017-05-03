# -*- coding: utf-8 -*-
import re
from django.conf import settings

from htmlmin.middleware import HtmlMinifyMiddleware
from htmlmin.minify import html_minify


class AllinkHtmlMinifyMiddleware(HtmlMinifyMiddleware):

    def process_response(self, request, response):
        minify = getattr(settings, "HTML_MINIFY", not settings.DEBUG)
        keep_comments = getattr(settings, 'KEEP_COMMENTS_ON_MINIFYING', False)
        parser = getattr(settings, 'HTML_MIN_PARSER', 'html5lib')
        # if minify and self.can_minify_response(request, response) and hasattr(response, 'rendered_content'):
        #     response.content = html_minify(response.rendered_content,
        #                                    ignore_comments=not keep_comments,
        #                                    parser=parser)
        return response


class AllinkUrlRedirectMiddleware:
    """
    This middleware lets you match a specific url and redirect the request to a
    new url.
    You keep a tuple of url regex pattern/url redirect tuples on your site
    settings, example:
    URL_REDIRECTS = (
        (r'www\.example\.com/hello/$', 'http://hello.example.com/'),
        (r'www\.example2\.com/$', 'http://www.example.com/example2/'),
    )
    """
    def process_request(self, request):
        host = request.META['HTTP_HOST'] + request.META['PATH_INFO']
        if hasattr(settings, 'URL_REDIRECTS'):
            for url_pattern, redirect_url in settings.URL_REDIRECTS:
                regex = re.compile(url_pattern)
                if regex.match(host):
                    return HttpResponsePermanentRedirect(redirect_url)
