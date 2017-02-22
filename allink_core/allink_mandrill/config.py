

class MandrillConfig:
    def __init__(self):
        from django.conf import settings

        self.apikey = getattr(settings, 'MANDRILL_API_KEY')

        self.default_transactional_template_name = getattr(settings, 'MANDRILL_DEFAULT_TRANSACTIONAL_TEMPLATE', 'default')
        self.default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        self.default_to_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')

    def get_default_from_name(self):
        from django.contrib.sites.models import Site
        return Site.objects.get_current().name

    def get_google_analytics_domains(self):
        from django.contrib.sites.models import Site
        return Site.objects.get_current().domain

    def get_site_domain(self):
        from django.contrib.sites.models import Site
        return Site.objects.get_current().domain
