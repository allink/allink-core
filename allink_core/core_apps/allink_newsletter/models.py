from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from djangocms_text_ckeditor.fields import HTMLField

from allink_core.core.models import AllinkBaseFormPlugin
from allink_core.core.models.choices import SALUTATION_CHOICES


class NewsletterSignupLog(TimeStampedModel):
    """
    In this models all entries of the NewsletterSignupForm are Stored
    """
    salutation = models.IntegerField(
        _('Salutation'),
        choices=SALUTATION_CHOICES,
        blank=False,
        null=False

    )

    first_name = models.CharField(
        _('First Name'),
        max_length=255,
    )

    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
    )

    email = models.EmailField(
        _('E-Mail'),
    )

    allows_gdpr_email = models.BooleanField(
        _('consent for email dispatch')
    )

    allows_gdpr_direct_mailing = models.BooleanField(
        _('consent for direct mailings'),
        blank=True,
    )

    allows_gdpr_personalised_marketing = models.BooleanField(
        _('consent for personalised marketing'),
        blank=True,
    )


class NewsletterSignupPlugin(AllinkBaseFormPlugin):
    """
    In This model all instances of the CMSNewsletterSignupPlugin are stored.
    """
    audience_id = models.CharField(
        _('audience id'),
        max_length=255,
        help_text=_('This is the id of the Mailchimp Audience the user wil be subscribed to')
    )

    consent_text = HTMLField(
        _('consent text'),
        blank=True,
    )

    double_opt_in_enabled = models.BooleanField(
        _('Double-Opt-In'),
        blank=True,
        default=False,
        help_text=_(
            'If selected an email wil be sent where the user will have to confirm his subscribtion to the mailing list')
    )

    marketing_permission_email_id = models.CharField(
        _('Mailchimp Email ID'),
        max_length=64,
        blank=True,
        help_text=_('Get this id via Postman and only change it if you know what you are doing')
    )

    marketing_permission_personalised_marketing_id = models.CharField(
        _('Mailchimp Personalised Marketing ID'),
        max_length=64,
        blank=True,
        help_text=_('Get this id via Postman and only change it if you know what you are doing')
    )

    marketing_permission_direct_mailing_id = models.CharField(
        _('Mailchimp Direct Mailing ID'),
        max_length=64,
        blank=True,
        help_text=_('Get this id via Postman and only change it if you know what you are doing')
    )
