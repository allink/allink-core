from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from allink_core.core.test.factories import UserFactory
from django.test.testcases import TestCase
from .factories import AllinkLegacyLinkFactory
from ..utils import (
    pre_and_append_slash, sort_get_params, append_gclid, legacy_redirect, fetch_legacy_redirect_on_request_path,
    fetch_legacy_redirect_match_subpages_on_request_path, )


class LegacyRedirectUtils(TestCase):

    def test_pre_and_append_slash(self):
        path = 'some/incomplete-path?hello=3&you=foo'

        self.assertEqual(pre_and_append_slash(path), '/some/incomplete-path/?hello=3&you=foo')

    def test_sort_get_params(self):
        path = 'some/path/?C=3&a=1&b=Hello'
        self.assertEqual(sort_get_params(path), 'some/path/?a=1&b=Hello&C=3')

    def test_append_gclid(self):
        path = 'some/path/?C=3&a=1&b=Hello'
        original_get_params = {'gclid': '123'}
        self.assertEqual(append_gclid(path, original_get_params), 'some/path/?C=3&a=1&b=Hello&gclid=123')

        path = 'some/path/'
        original_get_params = {'gclid': '123'}
        self.assertEqual(append_gclid(path, original_get_params), 'some/path/?gclid=123')

    def test_fetch_legacy_redirect_on_request_path(self):
        expected_ll = AllinkLegacyLinkFactory(old='/some-path/')
        AllinkLegacyLinkFactory(old='/some-other')

        request = RequestFactory()
        self.assertEqual(fetch_legacy_redirect_on_request_path(request.get('/some-path/')), expected_ll)

    def test_fetch_legacy_redirect_on_request_path_get_params(self):
        expected_ll = AllinkLegacyLinkFactory(old='/some/path/?a=1&b=Hello&C=3')
        request = RequestFactory()
        self.assertEqual(fetch_legacy_redirect_on_request_path(request.get('/some/path/?a=1&b=Hello&C=3')),
                         expected_ll)

    def test_fetch_legacy_redirect_on_request_path_does_not_exists(self):
        AllinkLegacyLinkFactory(old='/some-path/')
        request = RequestFactory()
        self.assertIsNone(fetch_legacy_redirect_on_request_path(request.get('/some-other')))

    def test_fetch_legacy_redirect_match_subpages_on_request_path(self):
        AllinkLegacyLinkFactory(old='/some-path/', match_subpages=True)
        expected_ll = AllinkLegacyLinkFactory(old='/some-path/more/specific/', match_subpages=True)

        request = RequestFactory()
        self.assertEqual(
            fetch_legacy_redirect_match_subpages_on_request_path(request.get('/some-path/more/specific/match/')),
            expected_ll)

    def test_legacy_redirect_skip_redirect_when_logged_out_should_redirect(self):
        AllinkLegacyLinkFactory(old='/some-path/', overwrite='/new-path/', skip_redirect_when_logged_in=True)

        request = RequestFactory().get('/some-path/')
        request.user = AnonymousUser()
        response = HttpResponse(content='dummy')

        self.assertEqual(legacy_redirect(request, response).status_code, 301)

    def test_legacy_redirect_skip_redirect_when_logged_in_should_redirect(self):
        AllinkLegacyLinkFactory(old='/some-path/', overwrite='/new-path/', skip_redirect_when_logged_in=True)

        request = RequestFactory().get('/some-path/')
        user = UserFactory()
        request.user = user
        self.client.force_login(user)
        response = HttpResponse(content='dummy')

        self.assertEqual(legacy_redirect(request, response).status_code, 200)
        self.assertEqual(legacy_redirect(request, response).content, b'dummy')
