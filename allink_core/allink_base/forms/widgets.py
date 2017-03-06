# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from django import forms
from django.conf import settings


class AdminPdfThumnailWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []

        if value:
            output.append(u'<img alt="%s" src="%s" height="200"/>' % (value.url, value.url,))
        else:
            output.append(_(u'Thumbnail is created when publication is saved. And a PDF document is assigned.'))

        # This is commented out b/c maybe you want to be able to override the thumbnail?
        # output.append(super(AdminFileWidget, self).render(name, value, attrs))

        return mark_safe(u''.join(output))


class Icon(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super(Icon, self).render(name, value, attrs=attrs, **kwargs)
        if value is None:
            value = ''
        iconset = value.split('-')[0] if value and '-' in value else ''
        iconset_prefexes = [s[1] for s in settings.PROJECT_ICONSETS]
        if len(settings.PROJECT_ICONSETS) and iconset not in iconset_prefexes:
            # invalid iconset! maybe because the iconset was removed from
            # the project. set it to the first in the list.
            iconset = settings.PROJECT_ICONSETS[0][1]
        from django.template.loader import render_to_string
        rendered = render_to_string(
            'admin/djangocms_button_link/widgets/icon.html',
            {
                'input_html': input_html,
                'value': value,
                'name': name,
                'iconset': iconset,
                'is_required': self.is_required,
                'iconsets': settings.PROJECT_ICONSETS,
            },
        )
        return rendered


