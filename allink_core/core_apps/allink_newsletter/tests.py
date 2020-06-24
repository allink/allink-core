import json
from http import HTTPStatus
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from django.conf import settings
from .base import AllinkMailchimp, MailchimpException


class AllinkMailchimpTestCase(TestCase):
    @override_settings(MAILCHIMP_DATACENTER='usXX')
    @override_settings(MAILCHIMP_API_KEY='API_KEY')
    def setUp(self):
        super().setUp()
        self.obj = AllinkMailchimp()

        # All the possible Failure codes the Mailchimp API can respond with.
        self.mailchimp_failure_codes = [400, 401, 403, 404, 405, 414, 422, 429, 500, 503]

        self.audience_id = 'ec9c7f47e1'
        self.email = 'test@allink.ch'
        self.hashed_email = '337bc5c62a21c06f556a2fe949e38bae'
        self.first_name = 'Vorname'
        self.last_name = 'Nachname'
        self.allows_gdpr_email = True
        self.allows_gdpr_personalised_marketing = True
        self.allows_gdpr_direct_mailing = False
        self.salutation = 'Mr.'
        self.double_opt_in_status = 'subscribed'
        self.mailchimp_api_key = settings.MAILCHIMP_API_KEY
        self.marketing_permission_email_id = 'dec570c690'
        self.marketing_permission_personalised_marketing_id = '7858abfe9e'
        self.marketing_permission_direct_mailing_id = '40ca9b0f52'
        self.mailchimp_datacenter = settings.MAILCHIMP_DATACENTER

    def subscribe_to_mailchimp_params(self):
        return self.salutation, \
               self.first_name, \
               self.last_name, \
               self.email, \
               self.allows_gdpr_email, \
               self.allows_gdpr_personalised_marketing, \
               self.allows_gdpr_direct_mailing, \
               self.audience_id, \
               self.mailchimp_api_key, \
               self.double_opt_in_status, \
               self.marketing_permission_email_id, \
               self.marketing_permission_personalised_marketing_id, \
               self.marketing_permission_direct_mailing_id, \
               self.mailchimp_datacenter

    def put_marketing_permission_params(self):
        return self.hashed_email, \
               self.allows_gdpr_email, \
               self.allows_gdpr_personalised_marketing, \
               self.allows_gdpr_direct_mailing, \
               self.audience_id, \
               self.mailchimp_api_key, \
               self.marketing_permission_email_id, \
               self.marketing_permission_personalised_marketing_id, \
               self.marketing_permission_direct_mailing_id, \
               self.mailchimp_datacenter

    def test_generation_of_hash(self):
        """
        We test whether or not our hash function, _get_subscriber_hash() returns the expected md5 hash of a
        given emailaddress

        """
        self.assertEqual(self.obj._generate_subscriber_hash(email=self.email), '337bc5c62a21c06f556a2fe949e38bae')

    def test_get_data(self):
        """
        We Test whether or not the _get_data method returns the expected object.
        """
        obj = AllinkMailchimp()
        data = {
            "email_address": self.email,
            "status": self.double_opt_in_status,
            "merge_fields": {
                "GENDER": self.salutation,
                "FNAME": self.first_name,
                "LNAME": self.last_name,
            }
        }
        data = json.dumps(data)
        self.assertEqual(
            obj._get_data(self.email, self.salutation, self.first_name, self.last_name, self.double_opt_in_status),
            data)

    @patch('requests.put')
    def test_subscribe_to_audience_api_error(self, mock_put):
        """
        we test the subscrive_to_audience() methods response when it is confronted with a failure code from the
        Mailchimp API
        It is expected to raise a MailchimpException

        """
        for failure_code in self.mailchimp_failure_codes:
            mock = Mock()
            mock.status_code = failure_code
            mock_put.return_value = mock
            with self.assertRaises(MailchimpException):
                self.obj.subscribe_to_audience(*self.subscribe_to_mailchimp_params())

    @patch('requests.put')
    def test_subscribe_to_audience_ok(self, mock_put):
        """
        We test if the subscribe_to_audience() method returns the correct value when handed with a correct response
        by the Mailchimp API
        """
        mock = Mock()
        mock.status_code = HTTPStatus.OK
        mock_put.return_value = mock
        self.assertEqual(HTTPStatus.OK,
                         self.obj.subscribe_to_audience(*self.subscribe_to_mailchimp_params()).status_code)

    @patch('requests.put')
    def test_put_marketing_permissions_api_error(self, mock_put):
        """
        we test the _put_marketing_permissions() methods response when it is confronted with a failure code from the
        Mailchimp API
        It is expected to raise a MailchimpException

        """
        for failure_code in self.mailchimp_failure_codes:
            mock = Mock()
            mock.status_code = failure_code
            mock_put.return_value = mock
            with self.assertRaises(MailchimpException):
                self.obj._put_marketing_permissions(*self.put_marketing_permission_params())

    @patch('requests.put')
    def test_put_marketing_permissions_ok(self, mock_put):
        """
        We test if the _put_marketing_permissions() method returns the correct value when handed with a correct response
        by the Mailchimp API
        """
        mock = Mock()
        mock.status_code = HTTPStatus.OK
        mock_put.return_value = mock
        self.assertEqual(HTTPStatus.OK,
                         self.obj._put_marketing_permissions(*self.put_marketing_permission_params()).status_code)

    def test_check_mailchimp_reponse_error(self):
        """
        In this test we test whether or not our check_mailchimp_response
        method raises a MailchimpException when it should.
        """
        for failure_code in self.mailchimp_failure_codes:
            mock = Mock()
            mock.status_code = failure_code
            with self.assertRaises(MailchimpException):
                self.obj._check_mailchimp_response(mock)

    def test_check_mailchimp_reponse_ok(self):
        """
        In this test we test whether or not our check_mailchimp_response
        method raises a MailchimpException when it shouldn't.
        """
        mock = Mock()
        mock.status_code = HTTPStatus.OK
        try:
            self.obj._check_mailchimp_response(mock)
        except MailchimpException:
            self.fail()
