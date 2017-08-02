# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError, RequestException

from django.contrib import messages
from django.conf import settings

from django.db import models
from django.utils.timezone import now
from django.utils.translation import activate, deactivate, ugettext_lazy as _
from allink_core.core.utils import base_url
from allink_core.core.models.models import AllinkInternalLinkFieldsModel


class AllinkLegacyLink(AllinkInternalLinkFieldsModel):
    old = models.CharField(_(u'Old Link'), max_length=255, unique=True)
    #  External Redirect
    overwrite = models.CharField(
        _(u'Overwrite Link'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(u'Overwrites \'New Page\', use for special urls that are not listed there')
    )

    active = models.BooleanField(
        _(u'Active'),
        default=True,
    )
    match_subpages = models.BooleanField(
        _(u'Match subpages'),
        default=False,
        help_text=_(u'If True, matches all subpages and redirects them to this link.')
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
    redirect_when_logged_out = models.BooleanField(
        _(u'Redirect when logged out'),
        default=False,
        help_text=_(u'If True, current site will not redirect when user is logged in. If False, the page will be redirected.')
    )
    language = models.CharField(
        _(u'Language'),
        max_length=200,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGES[0],
        null=True
    )

    class Meta:
        verbose_name = _('Legacy Link')
        verbose_name_plural = _('Legacy Links')

    def __str__(self):
        return self.old

    @property
    def link(self):
        if self.overwrite:
            return self.overwrite
        else:
            if self.language:
                activate(self.language)
                link = super(AllinkLegacyLink, self).link
                deactivate()
                return link

    def test_redirect(self, request):
        result = False
        old_url = base_url() + self.old
        new_path = self.link
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
                    if redir.status_code == 302:
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