import sys
import mandrill
from django.conf import settings
# from django.contrib.sites.models import Site


class MandrillConfig:
    def __init__(self):
        # self.apikey = getattr(settings, 'MANDRILL_API_KEY')

        self.default_transactional_template_name = getattr(settings, 'MANDRILL_DEFAULT_TRANSACTIONAL_TEMPLATE', 'default')
        self.default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        # self.default_from_name = Site.objects.get_current().name

        # self.google_analytics_domains = Site.objects.get_current().domain
        # self.site_domain = Site.objects.get_current().domain
