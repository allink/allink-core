# coding=utf-8
from django import forms
from parler.forms import TranslatableModelForm

from allink_core.core.loading import get_model


Members = get_model('members', 'Members')


class MembersAdminForm(TranslatableModelForm):

    class Meta:
        model = Members
        fields = ('member_nr', 'first_name', 'last_name', 'email', 'language')


class MembersProfileEditForm(forms.ModelForm):

    class Meta:
        model = Members
        fields = ('email', )
