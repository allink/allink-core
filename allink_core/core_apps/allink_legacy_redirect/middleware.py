from django.http import HttpResponsePermanentRedirect
from .utils import legacy_redirect


class AllinkLegacyRedirectMiddleware(object):
    """
    If the request matches one of the urls configured in AllinkLegacyLink a HttpResponsePermanentRedirect returned to
    the appropriate url.

    Google Click ids will be preserved.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return legacy_redirect(request, response)


