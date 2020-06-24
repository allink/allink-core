from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NewsletterSignupConfig(AppConfig):
    """
    We define the Verbose name in this config
    """
    name = 'allink_core.core_apps.allink_newsletter'
    verbose_name = _("Newsletter Signup")
