# -*- coding: utf-8 -*-
import requests
from urllib.parse import urldefrag
from requests.exceptions import ConnectionError, RequestException

from django.contrib import messages

from django.db import models
from django.utils.timezone import now
from django.utils.translation import activate, deactivate
from allink_core.core.utils import base_url
from allink_core.core_apps.allink_legacy_redirect.utils import sort_get_params, pre_and_append_slash
from allink_core.core.models import AllinkInternalLinkFieldsModel

__all__ = ['AllinkLegacyLink']


class AllinkLegacyLink(AllinkInternalLinkFieldsModel):
    old = models.CharField('Old Link', max_length=255, unique=True,
                           help_text='We strip away the anchor part of the URL as '
                                     'this part is not passed to the server.')

    #  External Redirect
    overwrite = models.CharField(
        'Overwrite Link',
        max_length=255,
        null=True,
        blank=True,
        help_text='Overwrites \'New Page\', use for special urls that are not listed there'
    )

    active = models.BooleanField(
        'Active',
        default=True,
    )
    match_subpages = models.BooleanField(
        'Match subpages',
        default=False,
        help_text='If True, matches all subpages and redirects them to this link.'
    )
    last_test_result = models.NullBooleanField(
        'Result of last test',
        default=None,
        help_text='Was the last automatic test successfull? (True = Yes, False = No, None = Not yet tested)'
    )
    last_test_date = models.DateTimeField(
        'Date of last test',
        null=True,
        blank=True
    )
    skip_redirect_when_logged_in = models.BooleanField(
        'Skip redirect when logged in',
        default=False,
        help_text=('If True, current site will not redirect when user is logged in. '
                   'If False, the page will be redirected.')
    )
    language = models.CharField(
        'Language',
        max_length=200,
        null=True
    )

    class Meta:
        verbose_name = 'Legacy Link'
        verbose_name_plural = 'Legacy Links'

    def __str__(self):
        return self.old

    def save(self, *args, **kwargs):
        self.old = urldefrag(self.old)[0]
        self.old = pre_and_append_slash(self.old)
        self.old = sort_get_params(self.old)
        super(AllinkLegacyLink, self).save(*args, **kwargs)

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
                'Can\'t connect to url: {}'.format(old_url)
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
                        location = redir.headers.get('Location')
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
