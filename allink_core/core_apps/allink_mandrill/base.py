# -*- coding: utf-8 -*-
import mandrill
from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.utils.dateformat import DateFormat
from raven import Client

from allink_core.core.utils import base_url
from allink_core.core.utils import get_display
from allink_core.core_apps.allink_mandrill.config import MandrillConfig
from allink_core.core_apps.allink_mandrill.helpers import check_result_status


class AllinkMandrillEmailBase:
    """
    Sends emails with mandrill.
    The only thing you have to specify is "template_name" the rest of the attributes are optional.

    have a look at the ./README.md for a basic guide on how to implement this class.
    """
    # The template can be sent with two types of merge var language settings
    MERGE_LANG_MAILCHIMP = 'mailchimp'  # Notation: *|FIRST_NAME|*
    MAILCHIMP_FORMAT = "*|{}|*"
    MERGE_LANG_HANDELBAR = 'handlebars'  # Notation: {FIRST_NAME}
    HANDELBAR_FORMAT = "{{{}}}"
    MERGE_FORMAT = {
        MERGE_LANG_MAILCHIMP: MAILCHIMP_FORMAT,
        MERGE_LANG_HANDELBAR: HANDELBAR_FORMAT,

    }
    template_name = None
    # Optional attributes
    merge_language = MERGE_LANG_MAILCHIMP
    translated = True
    google_analytics_campaign = None
    view_content_link = True
    # to make this as flexible as possible we added all the settings options of the Mandrill api message to the attrs
    # I have never seen these changed but if necessary you can do this here
    return_path_domain = None
    preserve_recipients = True
    inline_css = True
    auto_html = None
    auto_text = None

    def __init__(self, template_name=None, logging=False, language=None, async=False, send_with_celery=False,
                 track_clicks=True, track_opens=True, *args, **kwargs):
        """
        Args:
            template_name: mandrill template name (if translated=True, do not add the "_de")
            logging: Boolean if logging is turned on or nor if true implement
                def log(self, kwargs**)
        """
        self.config = MandrillConfig()
        self.logging = logging
        if self.translated:
            assert (language, 'You have to provide a language, if you send a translated email.')
            self.language = language
        self.async = async
        self.send_with_celery = send_with_celery
        if template_name:
            self.template_name = template_name
        self.track_opens = track_opens
        self.track_clicks = track_clicks

    @staticmethod
    def create_global_merge_var(template_keyword, content):
        """
        Args:
            template_keyword: Template Keyword used by Mandrill
            content: Content for this Template Keword

        Returns: Formatted object that meets requirements  for Mandrill API
                {'name': template_keyword, 'content': str(content)}
        """
        # JavaScript expects True like this "true" so we need this thingy
        if content == "False":
            return {'name': str(template_keyword), 'content': False}
        elif content == "True":
            return {'name': str(template_keyword), 'content': True}

        return {'name': str(template_keyword), 'content': str(content)}

    @staticmethod
    def create_email_to_entry(email_address, name):
        return {
            'email': email_address,
            'name': name,
            'type': 'to'
        }

    @staticmethod
    def replace_linebreaks_with_html(content):
        r = '<br />'
        return content.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)

    def build_subject(self):
        raise NotImplementedError

    def build_body(self):
        raise NotImplementedError

    def get_from_mail_address(self):
        raise NotImplementedError

    def fetch_to_email_addresses(self):
        raise NotImplementedError

    def log(self, **kwargs):
        # this is only needed if self.logging==True
        raise NotImplementedError

    def get_language(self):
        return self.language

    def get_template_name(self):
        assert self.template_name
        if not self.translated:
            return self.template_name
        if self.language:
            template_name = '{}_{}'.format(self.template_name, self.get_language())
        return template_name

    def get_from_name(self):
        return self.config.get_default_from_name()

    def get_website_for_metadata(self):
        return self.config.get_site_domain()

    def get_reply_to_email_address(self):
        return self.get_from_mail_address()

    def get_googleanalytics_domains(self):
        return [self.config.get_site_domain(), ]

    def send_transactional_email(self, message, template_content):
        if self.send_with_celery:

            from .tasks import send_transactional_mail_celery

            template_name = self.get_template_name()
            send_transactional_mail_celery.apply_async(args=[template_name, message, template_content], queue='slow')

        else:
            try:
                mandrill_client = mandrill.Mandrill(self.config.apikey)
                result = mandrill_client.messages.send_template(template_name=self.get_template_name(),
                                                                template_content=template_content, message=message,
                                                                async=self.async)
                check_result_status(result)
            except:  # as we just push it to sentry we catch all the errors
                if not hasattr(settings, 'RAVEN_CONFIG'):
                    raise
                client = Client(settings.RAVEN_CONFIG.get('dsn'))
                client.captureException()
                # sentry is not configured on localhost
                if not settings.RAVEN_CONFIG.get('dsn'):
                    raise

    def send_mail(self):
        """
        This should never throw an exception. Instead it fails silently and sends exceptions to sentry.
        (So should never have to wrap your .send_mail() call in a try/ except.
        for a better handling of failed emails you should implement an appropriate log
        """
        if self.translated:
            prev_language = translation.get_language()
            translation.activate(self.language)
        try:
            template_content = [{}]
            # we can only send, when we have a email address
            if self.fetch_to_email_addresses() and not self.fetch_to_email_addresses() == '':
                message = {
                    'auto_html': self.auto_html,
                    'auto_text': self.auto_text,
                    'from_email': str(self._dev_mode_safe_from_adress()),
                    'from_name': str(self.get_from_name()),
                    'global_merge_vars': self.build_body(),
                    'google_analytics_campaign': self.google_analytics_campaign,
                    'google_analytics_domains': self.get_googleanalytics_domains(),
                    'headers': {'Reply-To': self.get_reply_to_email_address()},
                    'inline_css': self.inline_css,
                    'merge_language': self.merge_language,
                    'metadata': {'website': self.get_website_for_metadata()},
                    'preserve_recipients': self.preserve_recipients,
                    'return_path_domain': self.return_path_domain,
                    'subject': str(self.build_subject()),
                    'to': self._dev_mode_safe_to_adresses(),
                    'track_clicks': self.track_clicks,
                    'track_opens': self.track_opens,
                    'view_content_link': self.view_content_link,
                }

                self.send_transactional_email(message=message, template_content=template_content)
                # if logging is enabled the function log will be called. You will have to implement it
                if self.logging:
                    self.log(to=message['to'],
                             subject=message['subject'],
                             form=message['from_email'],
                             body_vars=message['global_merge_vars'],
                             full_message=message)
        finally:
            if self.translated:
                translation.activate(prev_language)

    def _fetch_to_email_adresses_dev_mode(self):
        """
        Do not override this method! (unless you really know that this is what you want.)
        """
        return [self.create_email_to_entry(email, 'allink Test')
                for email in settings.ALLINK_MANDRILL_DEV_MODE_TO_EMAIL_ADDRESSES]

    def _get_from_email_adress_dev_mode(self):
        """
        Do not override this method! (unless you really know that this is what you want.)
        """
        return settings.ALLINK_MANDRILL_DEV_MODE_FROM_EMAIL_ADDRESS

    def _dev_mode_safe_from_adress(self):
        """
        Do not override this method! (unless you really know that this is what you want.)
        """
        if settings.ALLINK_MANDRILL_DEV_MODE:
            return self._get_from_email_adress_dev_mode()
        else:
            return self.get_from_mail_address()

    def _dev_mode_safe_to_adresses(self):
        """
        Do not override this method! (unless you really know that this is what you want.)
        """
        if settings.ALLINK_MANDRILL_DEV_MODE:
            return self._fetch_to_email_adresses_dev_mode()
        else:
            return self.fetch_to_email_addresses()


class AllinkMandrillFormEmail(AllinkMandrillEmailBase):
    """
    Takes an additional parameter "form"
    - adds all form fields to the merge vars
    - adds a merge var "form_fields" (this will list all available form fields.
      and can be used in the mailchimp template as a reference)

    APPEND_OPTIONAL_FIELDS = False
      all empty fields won't be send to mandrill

    example implementation:
    class SomeEmail(AllinkMandrillFormEmail):
        template_name = 'entra_living_signup_confirmation'
        google_analytics_campaign = template_name

        def fetch_to_email_addresses(self):
            return [
                self.create_email_to_entry(
                    self.form.data.get('email'),
                    ''.format(self.form.fields.get('last_name'), self.form.fields.get('first_name'))
                ),
            ]

    SomeEmail(form=form, language=get_language()).send_mail()
    """
    APPEND_OPTIONAL_FIELDS = True

    def __init__(self, form, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = form

    def build_body(self):
        form_fields_merge_vars = self.get_merge_vars_from_form(self.form)

        body = form_fields_merge_vars
        body.append(self.create_global_merge_var('submitted_form_str',
                                                 self.get_submitted_form_str(
                                                     self.form, form_fields_merge_vars)))
        body.append(self.create_global_merge_var('submitted_form_url', self.get_submitted_form_url(self.form)))
        body.append((self.create_global_merge_var('list_of_available_merge_vars',
                                                  self.get_list_of_available_merge_vars(self.form))))
        return body

    def get_merge_vars_from_form(self, form):
        """
        returns a list with all the form fields as a merge vars dict
            [('name': 'foo', 'content': 'bar'), ..]
        """
        form_fields_merge_vars = []
        for field in form.fields:
            if form.data.get(field):
                if type(form.fields.get(field)) == forms.MultipleChoiceField:
                    selected_choices = []
                    for option in form.fields.get(field).choices:
                        name, title = option
                        if name in form.cleaned_data.get(field):
                            selected_choices.append(translation.gettext(title))
                    form_fields_merge_vars.append(self.create_global_merge_var(field, '<br>'.join(selected_choices)))
                elif type(form.fields.get(field)) == forms.DateField:
                    # date field
                    date = DateFormat(form.cleaned_data.get(field)).format('j. F Y')
                    form_fields_merge_vars.append(self.create_global_merge_var(field, date))
                elif hasattr(form.fields.get(field), 'choices'):
                    # model field choices
                    form_fields_merge_vars.append(self.create_global_merge_var(field, get_display(
                        form.data.get(field), form.fields.get(field).choices)))
                elif hasattr(form.fields.get(field).widget, 'choices'):
                    # form field choices
                    form_fields_merge_vars.append(
                        self.create_global_merge_var(field, get_display(form.data.get(field), form.fields.get(
                            field).widget.choices)))
                elif type(form.fields.get(field)) == forms.BooleanField:
                    # checkbox
                    form_fields_merge_vars.append(
                        self.create_global_merge_var(field, _('Yes') if True else _('No')))
                # TODO form.data.get(field) is empty
                # elif type(form.fields.get(field)) == forms.FileField:
                #     # file field
                #     file_link_str = '{}{}'.format(base_url(), form.cleaned_data.get(field).file.url)
                #     form_fields_merge_vars.append(
                #         self.create_global_merge_var(field, file_link_str))
                else:
                    form_fields_merge_vars.append(self.create_global_merge_var(field, form.data.get(field)))
            else:
                # form field empty (optional)
                if self.APPEND_OPTIONAL_FIELDS:
                    form_fields_merge_vars.append(self.create_global_merge_var(field, '—'))
        return form_fields_merge_vars

    def get_submitted_form_str(self, form, form_fields_merge_vars):
        """
        for convenience we add a merge var 'submitted_form'
        (can be used to display all the form fields at once, including labels and linebreaks)
            [('name': 'submitted_form', 'content': '<<string with all form fields and labels separated with <br>'), ..]
        """
        submitted_form_str = '<br>'.join(
            ['{}:<br>{}<br>'.format(form.fields.get(merge_var.get('name')).label,
                                    merge_var.get('content')) for merge_var in form_fields_merge_vars])
        return submitted_form_str

    def get_submitted_form_url(self, form):
        """
        we add a link to the submitted form (url to django admin)
            [('name': 'submitted_form_url', 'content': '<<absolute url to django admin>>'), ..]
        """
        submitted_form_url = '{}{}'.format(base_url(),
                                           reverse('admin:%s_%s_change' % (form.instance._meta.app_label,
                                                                           form.instance._meta.model_name),
                                                   args=[form.instance.id]))
        return submitted_form_url

    def get_list_of_available_merge_vars(self, form):
        """
        we add a merge var 'list_of_available_merge_vars' (can be used as a reference in mailchimp templates)
            [('name': 'form_fields', 'content': '<<string with all form fields separated with
            <br> and formatted in the merge_language>>'), ..]
        """
        form_fields_combined = '<br>'.join(
            [self.MERGE_FORMAT[self.merge_language].format(field) for field in form.fields]
        )
        return form_fields_combined


class AllinkMandrillFormPluginEmail(AllinkMandrillFormEmail):
    """
    Takes parameters "form" and "plugin". The Plugin needs to define at least the fields in AllinkBaseFormPlugin.
    The plugin defines the email subject, sender email address and the internal recipients.

    example implementation:
    class SomeInternalEmail(AllinkMandrillFormPluginEmail):
        template_name = 'entra_living_signup_confirmation'
        google_analytics_campaign = template_name

        def fetch_to_email_addresses(self):
            return [self.create_email_to_entry(email, self.config.get_default_from_name()) for email in self.plugin.internal_recipients]

    SomeInternalEmail(form=form, plugin=plugin, language=get_language()).send_mail()
    """

    def __init__(self, plugin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin = plugin

    def build_subject(self):
        return self.plugin.email_subject

    def get_from_mail_address(self):
        return self.plugin.from_email_address
