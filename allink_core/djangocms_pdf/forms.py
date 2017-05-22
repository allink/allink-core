# -*- coding: utf-8 -*-
from django import forms
from allink_core.djangocms_pdf.models import AllinkPdfPageBreakPlugin


class AllinkPdfPageBreakPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkPdfPageBreakPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
