# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError, RequestException

from django.contrib import messages
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _
from cms.models.fields import PageField
from allink_core.allink_base.utils import base_url


class AllinkLegacyLink(models.Model):

    old = models.CharField(_(u'Old Link'), max_length=255, unique=True)
    new = PageField(
        verbose_name=_(u'New Page'),
        null=True,
        on_delete=models.SET_NULL,
        help_text=_(u'If provided, overrides the external link.')
    )
    overwrite = models.CharField(
        _(u'Overwrite Link'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(u'Overwrites \'New Link\', use for special urls that are not listed there')
    )
    active = models.BooleanField(
        _(u'Active'),
        default=True,
    )
    match_subpages = models.BooleanField(
        _(u'Match subpages'),
        default=False,
        help_text=_(u'If True, matches all subpages and redirects them to this link')
    )
    last_test_result = models.NullBooleanField(
        _(u'Result of last test'),
        default=None,
        help_text=_(u'Was the last automatic test successfull? (True = Yes, False = No, None = Not yet tested)')
    )
    last_test_date = models.DateTimeField(
        _(u'Date of last test'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Legacy Link')
        verbose_name_plural = _('Legacy Links')

    def __unicode__(self):
        return self.old

    def test_redirect(self, request):
        result = False
        old_url = base_url() + self.old
        new_path = self.overwrite if self.overwrite else self.new.get_slug()
        new_url = base_url() + '/' + new_path
        try:
            resp = requests.get(old_url)
        except ConnectionError:
            messages.add_message(
                request,
                messages.ERROR,
                u'Can\'t connect to url: {}'.format(old_url)
            )
            result = None
        except RequestException as e:
            messages.add_message(request, messages.ERROR, '%s: %s' % (e, self.old))
            result = None
        else:
            # successfull request, test for history
            if resp.status_code == 200:

                try:
                    # first history entry should be the redirect
                    redir = resp.history[0]
                    if redir.status_code == 301:
                        location = redir.headers.get(u'Location')
                        # location of redirect has to match
                        # Django 1.9 will send back relative urls
                        # if run via dev server
                        # Both absolute and relative urls should
                        # be accounted for
                        # https://en.wikipedia.org/wiki/HTTP_location

                        if location == new_url or location == new_path:
                            result = True
                except IndexError:
                    pass
        self.last_test_result = result
        self.last_test_date = now()
        self.save()
        return result
