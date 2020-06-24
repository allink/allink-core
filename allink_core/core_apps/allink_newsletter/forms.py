from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.core.models.choices import SALUTATION_CHOICES
from allink_core.core_apps.allink_newsletter.models import NewsletterSignupLog

#this is the form for the NewsletterSignupLog Soem fields are specified but all are added to the form
class NewsletterSignupForm(forms.ModelForm):
    salutation = forms.ChoiceField(
        label=_('Salutation'),
        widget=forms.RadioSelect(),
        choices=SALUTATION_CHOICES
    )

    email = forms.EmailField(
        label=_('E-Mail')
    )

    allows_gdpr_email = forms.BooleanField(
        label=_('E-Mail'),
        required=True
    )

    allows_gdpr_direct_mailing = forms.BooleanField(
        label=_('Direct mailings'),
        required=False
    )


    allows_gdpr_personalised_marketing = forms.BooleanField(
        label=_('Personalised Marketing'),
        required=False
    )

    class Meta:
        model = NewsletterSignupLog
        fields = '__all__'