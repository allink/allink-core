# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from parler.forms import TranslatableModelForm


class AllinkBaseModelForm(forms.ModelForm):
    pass

class AllinkBaseTranslatableModelForm(TranslatableModelForm):
    pass


# class AllinkBaseRegistrationForm(AllinkBaseModelForm):
#     """
#      feed it with a model
#      and you are good to go
#       model =
#     """
#     terms_accepted = forms.BooleanField(label=_(u'Terms of Service'), required=True)
#
#     class Meta:
#         model = None
#         widgets = {
#             'event': forms.HiddenInput(),
#             'terms': forms.HiddenInput(),
#             'terms_accepted': forms.CheckboxInput()
#         }
#         fields = ('event', 'terms', 'first_name', 'last_name', 'email', 'street', 'zip_code', 'place', 'terms_accepted')
#
#     def __init__(self, *args, **kwargs):
#         super(AllinkBaseRegistrationForm, self).__init__(*args, **kwargs)
#         #  all fiels should be required
#         for key in self.fields:
#             self.fields[key].required = True
