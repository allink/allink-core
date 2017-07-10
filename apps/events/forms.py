# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from allink_core.core.forms.forms import AllinkBaseModelForm
from allink_core.core_apps.allink_terms.models import AllinkTerms
from allink_core.core.loading import get_model

EventsRegistration = get_model('events', 'EventsRegistration')


class EventsRegistrationForm(AllinkBaseModelForm):

    class Meta:
        model = EventsRegistration
        widgets = {
            'event': forms.HiddenInput(),

        }
        fields = ('event', 'salutation', 'first_name', 'last_name', 'company_name', 'email', 'phone', 'message')

# for reference
# class EventsRegistrationTermsForm(AllinkBaseModelForm):
#
#     terms_accepted = forms.BooleanField(label=_(u'Terms of Service'), required=True)
#
#     class Meta:
#         model = EventsRegistration
#         widgets = {
#             'event': forms.HiddenInput(),
#             'terms': forms.HiddenInput(),
#             'terms_accepted': forms.CheckboxInput()
#
#         }
#         fields = ('event', 'salutation', 'first_name', 'last_name', 'company_name', 'email', 'phone', 'message', 'terms', 'terms_accepted')
#
#     def __init__(self, *args, **kwargs):
#         super(EventsRegistrationTermsForm, self).__init__(*args, **kwargs)
#         try:
#             self.fields['terms_accepted'].label = mark_safe(_('I have read and accept the <a href="%s" target="_blank">terms and conditions.</a>')) % (AllinkTerms.objects.get_published().terms_cms_page.get_absolute_url())
#             self.fields['terms'].initial = AllinkTerms.objects.get_published()
#         except:
#             raise AttributeError(_(u'Please configure Terms. And create the corresponding cms Page.'))
