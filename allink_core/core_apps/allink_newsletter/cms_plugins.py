from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseFormPlugin
from allink_core.core_apps.allink_newsletter.forms import NewsletterSignupForm
from allink_core.core_apps.allink_newsletter.models import NewsletterSignupPlugin
from django.utils.translation import ugettext_lazy as _


@plugin_pool.register_plugin
class CMSAllinkNewsletterSignupPlugin(CMSAllinkBaseFormPlugin):
    """
    Here we register the CMS Plugin
    """
    name = _('Newsletter Signup Plugin')
    model = NewsletterSignupPlugin
    render_template = 'allink_newsletter/content.html'
    cache = False

    form_class = NewsletterSignupForm
    url_name = 'signup'

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update({
            'form': self.form_class(),
            'action': self.get_form_action(instance),
        })
        return context
