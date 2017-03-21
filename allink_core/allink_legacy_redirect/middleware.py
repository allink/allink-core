from django.http import HttpResponsePermanentRedirect
from django.db.models import Q

from .models import AllinkLegacyLink


class AllinkLegacyRedirectMiddleware(object):
    """
    Perma-redirect old links to their new site,
    stripping all GET-params (except google click id)
    """
    def process_request(self, request):
        try:
            link = AllinkLegacyLink.objects.get(Q(old=request.path) | Q(old=request.path + '/'))
        # check for links which match subpages
        except AllinkLegacyLink.DoesNotExist:
            # build up array with path parts
            # e.g. [u'en', u'agency', u'contact']
            path_bits = request.path.split('/')[1:-1]
            length = len(path_bits)
            olds = []

            # omit final bit because we already
            # tested for it in our first try
            # e.g. [u'/en/', u'/en/agency/']
            for i in range(1, length):
                olds.append('/%s/' % ('/').join(path_bits[:i]))

            # if we got multiple links with match_subpages
            # enabled (e.g. /en/ and /en/agency/), return
            # the longer one
            link = AllinkLegacyLink.objects.filter(old__in=olds, match_subpages=True).order_by('old').last()
        if not link or not link.active:
            return

        # 'overwrite' takes priority over 'new'
        if link.overwrite:
            new_link = link.overwrite
        elif link.new:
            new_link = link.new_page
        else:
            return

        # preserve Google Click Identifier
        if 'gclid' in request.GET:
            new_link += '?gclid=%s' % request.GET['gclid']
        return HttpResponsePermanentRedirect(new_link)
