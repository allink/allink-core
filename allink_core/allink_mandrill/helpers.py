# -*- coding: utf-8 -*-
import mandrill
from raven import Client
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from .config import MandrillConfig

config = MandrillConfig()

def check_result_status(result):
   if result[0].get('status') != 'sent' and result[0].get('status') != 'queued':
       raise mandrill.Error(
           _(u"Mandrill hasn't raised an error but email could not been sent. (status: '{}', reason: '{}')")
               .format(result[0].get('status'), result[0].get('reject_reason')))


def send_transactional_email(message, template_content, language=None, translated=False, template_name=None, async=False):

    if not template_name:
        template_name = config.default_transactional_template_name
    if not language and translated:
        template_name = '{}_{}'.format(template_name, get_language())
    if language:
        template_name = '{}_{}'.format(template_name, language)

    try:
        mandrill_client = mandrill.Mandrill(getattr(settings, 'MANDRILL_API_KEY'))
        result = mandrill_client.messages.send_template(template_name=template_name, template_content=template_content, message=message, async=async)
        check_result_status(result)
    except mandrill.Error:
        client = Client(settings.RAVEN_CONFIG.get('dns'))
        client.captureException()
        # sentry is not configured on localhost
        if not settings.RAVEN_CONFIG.get('dns'):
            raise




