# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django import forms


class ContextRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        from django.template.loader import render_to_string
        rendered = render_to_string(
            'admin/djangocms_button_link/widgets/context.html',
            {'selects': self},
        )
        return rendered


class Context(forms.widgets.RadioSelect):
    renderer = ContextRenderer


class SizeRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        from django.template.loader import render_to_string
        rendered = render_to_string(
            'admin/djangocms_button_link/widgets/size.html',
            {'selects': self},
        )
        return rendered


class Size(forms.widgets.RadioSelect):
    renderer = SizeRenderer


class MiniTextarea(forms.widgets.Textarea):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['cols'] = '120'
        attrs['rows'] = '1'
        super(MiniTextarea, self).__init__(attrs)


class LinkOrButtonRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        from django.template.loader import render_to_string
        rendered = render_to_string(
            'admin/djangocms_button_link/widgets/link_or_button.html',
            {'selects': self},
        )
        return rendered


class LinkOrButton(forms.widgets.RadioSelect):
    renderer = LinkOrButtonRenderer
