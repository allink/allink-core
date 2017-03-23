from django.http import HttpResponsePermanentRedirect
from django.db.models import Q

from itertools import combinations, permutations

from .models import AllinkLegacyLink


class AllinkLegacyRedirectMiddleware(object):
    """
    Perma-redirect old links to their new site (except google click id)
    """

    def process_request(self, request):
        has_get_parameters = False
        link = None
        try:
            link = AllinkLegacyLink.objects.get(Q(old=request.path) | Q(
                old=request.path + '/') | Q(old=request.get_full_path()), active=True)

        except AllinkLegacyLink.DoesNotExist:
            # Here we handle the case that the old url
            # can have GET parameters, and some of them but not all
            # are used to specify a redirection
            for i in range(len(request.GET) - 1, 0, -1):
                possible_olds = []
                # we need to check all permutations for all subsets
                # of GET parameters. First we check the most
                # specific ones. That means the ones with
                # all but one parameter. (All parameters are
                # already checked with "get_full_path" in the first
                # query on top.)
                combis = combinations(request.GET.items(), i)
                perms = [permutations(combi) for combi in combis]
                for perm in perms:
                    for get_parameters in perm:
                        possible_olds.append(request.path + '?' + '&'.join(['%s=%s' % (param, value) for param, value in get_parameters]))
                        possible_olds.append(request.path + '/?' + '&'.join(['%s=%s' % (param, value) for param, value in get_parameters]))
                    try:
                        link = AllinkLegacyLink.objects.get(old__in=possible_olds, active=True)
                        has_get_parameters = True
                        break
                    except AllinkLegacyLink.DoesNotExist:
                        continue

        if not link:
            # check for links which match subpages
            # this must be done after the GET parameter checks,
            # cause subpages are less specific.

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
            link = AllinkLegacyLink.objects.filter(old__in=olds, match_subpages=True, active=True).order_by('old').last()

        if not link:
            return

        # 'overwrite' takes priority over 'new'
        if link.overwrite:
            new_link = link.overwrite
        elif link.new_page:
            new_link = link.new_page
        else:
            return

        # preserve Google Click Identifier
        if 'gclid' in request.GET:
            if has_get_parameters:
                new_link += '&gclid=%s' % request.GET['gclid']
            else:
                new_link += '?gclid=%s' % request.GET['gclid']
        return HttpResponsePermanentRedirect(new_link)
