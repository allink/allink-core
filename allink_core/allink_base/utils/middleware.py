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
