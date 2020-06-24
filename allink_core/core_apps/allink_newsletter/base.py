import json

import requests
import hashlib
from http import HTTPStatus


class MailchimpException(Exception):
    """
    This is our Exception for all thins Mailchimp.
    it is in the responsibility of the person using this class to handle this Exception
    """
    pass


class AllinkMailchimp(object):
    """
    This is our connection to the Mailchimp API 3.0
    We have an endpoint to subscribe users to a given mailchimp audience
    For now the subscribe_to_audience() method is the only thing you should use from outside this class.

    """

    def __init__(self):
        pass

    API_VERSION = '3.0'

    def subscribe_to_audience(self, salutation, first_name, last_name, email, allows_gdpr_email,
                              allows_gdpr_personalised_marketing, allows_gdpr_direct_mailing, audience_id,
                              mailchimp_api_key, double_opt_in_status, marketing_permission_email_id,
                              marketing_permission_personalised_marketing_id, marketing_permission_direct_mailing_id,
                              mailchimp_datacenter):
        """
        If given all parameters this method adds a user to an audience
        :param salutation: String
        :param first_name: String
        :param last_name: String
        :param email: String
        :param allows_gdpr_email: Boolean
        :param allows_gdpr_personalised_marketing: Boolean
        :param allows_gdpr_direct_mailing: Boolean
        :param audience_id: string
        :param mailchimp_api_key: String
        :param double_opt_in_status: string (subscribed or pending)
        :param marketing_permission_email_id: String (find this by connecting to your audience with postman)
        :param marketing_permission_personalised_marketing_id: String (find this by connecting to your audience with
        postman)
        :param marketing_permission_direct_mailing_id: String (find this by connecting to your audience with postman)
        :param mailchimp_datacenter: string (you find this at the end of your API-Key)
        :return: The Response object of the Mailchimp API if the request was successful, in case of an error a
        MailchimpException is raised but not handeld
        """
        hashed_email = self._generate_subscriber_hash(email)
        response = requests.put(
            'https://{}.api.mailchimp.com/3.0/lists/{}/members/{}/'.format(mailchimp_datacenter, audience_id,
                                                                           hashed_email),
            auth=('apikey', mailchimp_api_key),
            data=self._get_data(email, salutation, first_name, last_name, double_opt_in_status)
        )
        self._check_mailchimp_response(response)

        self._put_marketing_permissions(hashed_email, allows_gdpr_email, allows_gdpr_personalised_marketing,
                                        allows_gdpr_direct_mailing, audience_id, mailchimp_api_key,
                                        marketing_permission_email_id,
                                        marketing_permission_personalised_marketing_id,
                                        marketing_permission_direct_mailing_id, mailchimp_datacenter)
        return response

    def _generate_subscriber_hash(self, email):
        """
        This method hashes the lowercase encoded version of a given string and returns it in hexadecimals
        :param email: String
        :return: hexadecimal md5 hash of param email
        """
        cleaned_email = email.lower().encode()
        hashed_email = hashlib.md5(cleaned_email)
        return hashed_email.hexdigest()

    def _put_marketing_permissions(self, hashed_email, allows_gdpr_email, allows_gdpr_personalised_marketing,
                                   allows_gdpr_direct_mailing, audience_id, mailchimp_api_key,
                                   marketing_permission_email_id, marketing_permission_personalised_marketing_id,
                                   marketing_permission_direct_mailing_id, mailchimp_datacenter):
        """
        Here we update the marketing permission fields for a given user on a given audience.
        For this to work you have to provide all following parameters and GDPR Field have to be active on the audience
        If the Mailchimp API responds with an error response a MailchimpException is raised.
        :param hashed_email: md5 hash of an email
        :param allows_gdpr_email: Boolean
        :param allows_gdpr_personalised_marketing:Boolean
        :param allows_gdpr_direct_mailing: Boolean
        :param audience_id: String
        :param mailchimp_api_key:
        :param marketing_permission_email_id: String (find this by connecting to your audience with postman)
        :param marketing_permission_personalised_marketing_id:String (find this by connecting to your audience with
        postman)
        :param marketing_permission_direct_mailing_id: String (find this by connecting to your audience with postman)
        :param mailchimp_datacenter: String (you find this at the end of your API-Key)
        :return: The Response object of the Mailchimp API if the request was successful, in case of an error a
        MailchimpException is raised but not handeld
        """
        data = {
            "marketing_permissions": [
                {"marketing_permission_id": marketing_permission_email_id, "enabled": allows_gdpr_email},
                {"marketing_permission_id": marketing_permission_personalised_marketing_id,
                 "enabled": allows_gdpr_personalised_marketing},
                {"marketing_permission_id": marketing_permission_direct_mailing_id,
                 "enabled": allows_gdpr_direct_mailing}
            ]
        }
        data = json.dumps(data)

        response = requests.put(
            'https://{}.api.mailchimp.com/{}/lists/{}/members/{}'.format(mailchimp_datacenter, self.API_VERSION,
                                                                         audience_id, hashed_email),
            auth=('apikey', mailchimp_api_key), data=data
        )
        self._check_mailchimp_response(response)
        return response

    def _get_data(self, email, salutation, first_name, last_name, double_opt_in_status):
        """
        In this method we populate a dict with the given parameters
        :param email: String
        :param salutation: String
        :param first_name: String
        :param last_name: String
        :param double_opt_in_status: string (subscribed or pending)
        :return: the json of the populated dict.
        """
        data = {
            "email_address": email,
            "status": double_opt_in_status,
            "merge_fields": {
                "GENDER": salutation,
                "FNAME": first_name,
                "LNAME": last_name,
            }
        }
        return json.dumps(data)

    def _check_mailchimp_response(self, response):
        """
        Here we check whether the reponse od the Mailchimp API was valid. If not we raise a MailchimpException
        :param response: response object with a property status_code
        """
        if response.status_code != HTTPStatus.OK:
            raise MailchimpException(response.json())
