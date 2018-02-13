# -*- coding: utf-8 -*-
from django.core.exceptions import AppRegistryNotReady


class MandrillConfig:
    def __init__(self):
        from django.conf import settings
        from allink_core.core.loading import get_model

        try:
            config = get_model('config', 'Config').get_solo()
        except AppRegistryNotReady:
            config = None

        self.apikey = getattr(settings, 'MANDRILL_API_KEY')

        self.default_transactional_template_name = getattr(settings, 'MANDRILL_DEFAULT_TRANSACTIONAL_TEMPLATE', 'default')
        self.default_from_email = getattr(config, 'default_from_email', 'itcrowd@allink.ch')
        self.default_to_email = getattr(config, 'default_to_email', 'itcrowd@allink.ch')

    def get_default_from_name(self):
        from django.contrib.sites.models import Site
        return Site.objects.get_current().name

    def get_google_analytics_domains(self):
        from django.contrib.sites.models import Site
        return Site.objects.get_current().domain

    def get_site_domain(self):
        from django.contrib.sites.models import Site
        return Site.objects.get_current().domain
