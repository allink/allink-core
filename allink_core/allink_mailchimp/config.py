import sys
from django.conf import settings

class MailChimpConfig:
    def __init__(self):

        apikey = getattr(settings, 'MAILCHIMP_API_KEY', '')

        try:
            parts = apikey.split('-')
            if len(parts) != 2:
                print "This doesn't look like an API Key: " + apikey
                print "The API Key should have both a key and a server name, separated by a dash, like this: abcdefg8abcdefg6abcdefg4-us1"
                sys.exit()

            self.shard = parts[1]
            self.api_root = "https://" + self.shard + ".api.mailchimp.com/3.0/"
        except:
            pass
        # SETTINGS
        self.apikey = apikey
        self.default_list_id = getattr(settings, 'MAILCHIMP_DEFAULT_LIST_ID', None)
        self.signup_form = getattr(settings, 'MAILCHIMP_SIGNUP_FORM', None)
        self.additional_fields = getattr(settings, 'MAILCHIMP_ADDITIONAL_FIELDS', {})
        """
        settings.MAILCHIMP_DOUBLE_OPTIN
        - if set to True a Welcome Email will be sent and the double opt-in process will be used
        - if set to False no Welcome Email will be sent and the user gets subscribed directly to the list
        """
        self.double_optin = getattr(settings, 'MAILCHIMP_DOUBLE_OPTIN', False)
