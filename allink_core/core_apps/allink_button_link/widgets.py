# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django import forms


class Context(forms.widgets.RadioSelect):
    template_name = 'admin/allink_button_link/widgets/context.html'


class Size(forms.widgets.RadioSelect):
    template_name = 'admin/allink_button_link/widgets/size.html'


class MiniTextarea(forms.widgets.Textarea):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['cols'] = '120'
        attrs['rows'] = '1'
        super(MiniTextarea, self).__init__(attrs)


class LinkOrButtonRenderer(forms.widgets.RadioSelect):
    def render(self):
        from django.template.loader import render_to_string
        rendered = render_to_string(
            'admin/allink_button_link/widgets/link_or_button.html',
            {'selects': self},
        )
        return rendered


class LinkOrButton(forms.widgets.RadioSelect):
    renderer = LinkOrButtonRenderer
