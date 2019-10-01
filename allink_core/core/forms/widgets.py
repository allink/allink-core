# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings
from django import forms
from webpack_loader.utils import get_files

from allink_core.core.utils import get_project_color_choices
from allink_core.core.admin.mixins import AllinkMediaAdminMixin


class AdminPdfThumnailWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []

        if value:
            output.append('<img alt="%s" src="%s" height="200"/>' % (value.url, value.url,))
        else:
            output.append('Thumbnail is created when publication is saved. And a PDF document is assigned.')

        # This is commented out b/c maybe you want to be able to override the thumbnail?
        # output.append(super(AdminFileWidget, self).render(name, value, attrs))

        return mark_safe(''.join(output))


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
            'admin/allink_button_link/widgets/icon.html',
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


class SpectrumColorPicker(AllinkMediaAdminMixin, forms.widgets.TextInput):
    """
    Based on Brian Grinstead's Spectrum - http://bgrins.github.com/spectrum/
    This widget is used to select a Project Color. With some few options
    in the pushed colorFields, it could be used more flexible if needed.
    """

    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop('default', None)
        super(SpectrumColorPicker, self).__init__(*args, **kwargs)

    def _get_project_color_choices(self):
        palette = ",".join("'%s'" % color for color in get_project_color_choices())
        if self.default:
            palette = "'%s'," % self.default + palette
        else:
            palette = palette + ",'transparent'"
        return palette

    def _render_js(self, _id, value):
        js = """
            <script type="text/javascript">
                document.addEventListener("DOMContentLoaded", function(event) {
                    if (!window.colorFields) {
                        window.colorFields = [];
                    }

                    window.colorFields.push({
                        id: '#%s',
                        color: "%s",
                        showPaletteOnly: true,
                        palette:[%s],
                        localStorageKey: "projectcolors"
                    });
                });
            </script>""" % (_id, value, self._get_project_color_choices())
        return js

    def render(self, name, value, attrs=None, renderer=None):
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        if value:
            for key, val in get_project_color_choices().items():
                if val == value:
                    value = key
                    break
        rendered = super(SpectrumColorPicker, self).render(name, value, attrs=attrs, renderer=None)
        return mark_safe(rendered + self._render_js(attrs['id'], value))


class SearchSelectWidget(AllinkMediaAdminMixin, forms.widgets.Select):

    def __init__(self, attrs=None, choices=()):
        class_attrs = {"data-live-search": "true", 'class': 'selectpicker'}
        if attrs:
            attrs.update(class_attrs)
        else:
            attrs = class_attrs
        super(SearchSelectWidget, self).__init__(attrs)
