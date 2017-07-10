# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from allauth.compat import reverse
from allauth.utils import build_absolute_uri
from allauth.account.utils import user_pk_to_url_str

from allink_core.core_apps.allink_mandrill.config import MandrillConfig

from allink_core.core_apps.allink_mandrill.helpers import send_transactional_email

config = MandrillConfig()


def send_welcome_email(request, member):
    # generate reset password url
    temp_key = default_token_generator.make_token(member.user)
    path = reverse("account_reset_password_from_key",
                   kwargs=dict(uidb36=user_pk_to_url_str(member.user),
                               key=temp_key))
    link = build_absolute_uri(request, path)

    subject = render_to_string('members/email/welcome_subject.txt')

    text = render_to_string('members/email/welcome_text.txt', {'set_password_link': link})
    r = '<br />'
    text = text.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)

    template_content = [{
        # 'content': 'example content',
        # 'name': 'example name'
    }]
    message = {
        # 'attachments': [{
        #     'content': 'ZXhhbXBsZSBmaWxl',
        #     'name': 'myfile.txt',
        #     'type': 'text/plain'
        # }],
        'auto_html': None,
        'auto_text': None,
        # 'bcc_address': 'message.bcc_address@example.com',
        'from_email': config.default_from_email,
        'from_name': 'MFGZ',
        'global_merge_vars': [
            {'name': 'first_name', 'content': member.first_name},
            {'name': 'last_name', 'content': member.last_name},
            {'name': 'text', 'content': text},
        ],
        # 'google_analytics_campaign': 'Member welcome email',
        # 'google_analytics_domains': [config.google_analytics_domains],
        'headers': {'Reply-To': config.default_from_email},
        # 'html': '<p>Example HTML content</p>',
        # 'images': [{
        #     'content': 'ZXhhbXBsZSBmaWxl',
        #     'name': 'IMAGECID',
        #     'type': 'image/png'
        # }],
        # 'important': False,
        'inline_css': True,
        'merge': True,
        'merge_language': 'mailchimp',
        # 'merge_vars': [{
        #     'rcpt': 'recipient.email@example.com',
        #     'vars': [{
        #         'content': 'merge2 content', 'name': 'merge2'
        #     }]
        # }],
        # 'metadata': {'website': config.site_domain},
        'preserve_recipients': True,
        # 'recipient_metadata': [{
        #     'rcpt': 'recipient.email@example.com',
        #     'values': {'user_id': 123456}}],
        'return_path_domain': None,
        # 'signing_domain': None,
        # 'subaccount': 'customer-123',
        'subject': subject,
        # 'tags': ['password-resets'],
        # 'text': plain_text,
        'to': [{
            'email': member.email,
            'name': member.full_name,
            'type': 'to'
        }],
        'track_clicks': True,
        'track_opens': True
        # 'tracking_domain': None,
        # 'url_strip_qs': None,
        # 'view_content_link': None
    }

    send_transactional_email(message=message, template_name='mfgz_default', template_content=template_content)
    member.log('welcome_email_sent', u'Welcome email sent.')


def send_member_modified_email(member):

    logourl = 'https://mfgz-allink-stage.eu.aldryn.io/static/images/branding/mfgz-logo-web.svg'
    subject = render_to_string('members/email/member_modified_subject.txt')
    text = render_to_string('members/email/member_modified_text.txt', {'member_nr': member.member_nr, 'member_email': member.email})
    r = '<br />'
    text = text.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)

    template_content = [{
        # 'content': 'example content',
        # 'name': 'example name'
    }]
    message = {
        # 'attachments': [{
        #     'content': 'ZXhhbXBsZSBmaWxl',
        #     'name': 'myfile.txt',
        #     'type': 'text/plain'
        # }],
        'auto_html': None,
        'auto_text': None,
        # 'bcc_address': 'message.bcc_address@example.com',
        'from_email': config.default_from_email,
        # 'from_name': config.default_from_name,
        'global_merge_vars': [
            {'name': 'logourl', 'content': logourl},
            {'name': 'text', 'content': text},
        ],
        # 'google_analytics_campaign': 'Member welcome email',
        # 'google_analytics_domains': [config.google_analytics_domains],
        'headers': {'Reply-To': config.default_from_email},
        # 'html': '<p>Example HTML content</p>',
        # 'images': [{
        #     'content': 'ZXhhbXBsZSBmaWxl',
        #     'name': 'IMAGECID',
        #     'type': 'image/png'
        # }],
        # 'important': False,
        'inline_css': True,
        'merge': True,
        'merge_language': 'mailchimp',
        # 'merge_vars': [{
        #     'rcpt': 'recipient.email@example.com',
        #     'vars': [{
        #         'content': 'merge2 content', 'name': 'merge2'
        #     }]
        # }],
        # 'metadata': {'website': config.site_domain},
        'preserve_recipients': True,
        # 'recipient_metadata': [{
        #     'rcpt': 'recipient.email@example.com',
        #     'values': {'user_id': 123456}}],
        'return_path_domain': None,
        # 'signing_domain': None,
        # 'subaccount': 'customer-123',
        'subject': subject,
        # 'tags': ['password-resets'],
        # 'text': plain_text,
        'to': [{
            'email': config.default_from_email,
            'name': member.full_name,
            'type': 'to'
        }],
        'track_clicks': True,
        'track_opens': True
        # 'tracking_domain': None,
        # 'url_strip_qs': None,
        # 'view_content_link': None
    }

    send_transactional_email(message=message, template_content=template_content)
    member.log('member_modified_email_sent', u'Member modified email sent.')
