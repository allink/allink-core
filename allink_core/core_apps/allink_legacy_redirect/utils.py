from collections import OrderedDict
from urllib.parse import urlparse, urlunparse
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect


def sort_get_params(path):
    """
    sorts GET parameters alphabetically in a url
    """
    url = urlparse(path)
    if url.query:
        get_parameters = OrderedDict(gp.split("=") for gp in url.query.split("&"))
        sorted_get_parameters = dict(sorted(get_parameters.items(), key=lambda x: x[0].lower()))
        sorted_query_string = '&'.join(['%s=%s' % (key, value) for (key, value) in sorted_get_parameters.items()])
        url = url._replace(query=sorted_query_string)
    return urlunparse(url)


def pre_and_append_slash(path):
    url = urlparse(path)
    if not url.path.startswith('/'):
        url = url._replace(path='/' + url.path)
    if not url.path.endswith('/'):
        url = url._replace(path=url.path + '/')
    return urlunparse(url)


def append_gclid(path, get_params):
    """
    preserve Google Click Identifier in path
    """
    url = urlparse(path)

    if 'gclid' in get_params:
        base = url.query + '&' if url.query else url.query
        url = url._replace(query='{}gclid={}'.format(base, get_params['gclid']))
    return urlunparse(url)


def fetch_legacy_redirect_match_subpages_on_request_path(request):
    """
    check for links which match subpages
    this must be done after the check on an exact match (including) GET parameter, because subpages are less specific.
    :returns the first item in the queryset or None
    """
    from .models import AllinkLegacyLink

    # build up array with path parts
    # e.g. ['en','agency','contact']
    path_bits = request.path.split('/')[1:-1]
    length = len(path_bits)
    olds = []

    # omit final bit because we already
    # tested for it in our first try
    # e.g. ['/en/','/en/agency/']
    for i in range(1, length):
        olds.append('/%s/' % ('/').join(path_bits[:i]))

    # if we got multiple links with match_subpages
    # enabled (e.g. /en/ and /en/agency/), return
    # the longer one
    legacy_link = AllinkLegacyLink.objects.filter(
        old__in=olds,
        match_subpages=True,
        active=True
    ).order_by('old').last()

    return legacy_link


def fetch_legacy_redirect_on_request_path(request):
    """
    fetches LegacyLink from db if old path matches the request path
    :returns the first item in the queryset or None
    """
    from .models import AllinkLegacyLink

    legacy_link = AllinkLegacyLink.objects.filter(Q(old=request.get_full_path()), active=True).first()

    return legacy_link


def legacy_redirect(request, response):
    """
    Checks for a request if a corresponding entry in LegacyRedirect exist and
    :returns the appropriate HttpResponsePermanentRedirect response or the original response
    """
    legacy_link = fetch_legacy_redirect_on_request_path(request=request)

    if not legacy_link:
        legacy_link = fetch_legacy_redirect_match_subpages_on_request_path(request)

    if not legacy_link:
        return response

    # if user is logged in, skip redirect
    if legacy_link.skip_redirect_when_logged_in and request.user.is_authenticated:
        return response

    new_path = legacy_link.link
    new_path = append_gclid(new_path, request.GET)

    return HttpResponsePermanentRedirect(new_path)
