from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class NewsletterSignupApphook(CMSApp):
    """
    This is the Apphook for the allink_newsletter app
    """
    name = 'Newsletter Signup Apphook'
    app_name = 'allink_newsletter'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.core_apps.allink_newsletter.urls']


apphook_pool.register(NewsletterSignupApphook)
