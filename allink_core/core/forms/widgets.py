# -*- coding: utf-8 -*-
from itertools import chain

from django import forms
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings
import sortedm2m.forms

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


class SortedM2MWidget(sortedm2m.forms.SortedCheckboxSelectMultiple):
    """
    Copied from https://github.com/divio/aldryn-common

    Copied because this package is no longer maintained.
    https://github.com/divio/aldryn-common/commit/6582754be67390d056d4aaa1f799c183e808c914

    """

    template = 'widgets/sortedm2m_widget.html'

    def render(self, name, value, attrs=None, choices=()):
        # TODO: make a pull request to sortedm2m to make it easy to override the template
        # TODO: make a pull request to sortedm2m to make it easy to add the addtional
        # TODO: link to admin (or integrate this whole widget)
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)

        # Normalize to strings
        str_values = [force_text(v) for v in value]

        selected = []
        unselected = []

        # get the admin link
        rel_to = self.choices.queryset.model  # this is hacky
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())

        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = ' for="%s"' % conditional_escape(final_attrs['id'])
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_text(option_label))

            try:
                admin_url = reverse(
                    'admin:%s_%s_change' % info,
                    # current_app=self.admin_site.name,
                    args=(option_value,),
                )
            except NoReverseMatch:
                info = (
                    self.admin_site.root_path,
                    rel_to._meta.app_label,
                    rel_to._meta.object_name.lower(),
                    option_value,
                )
                admin_url = '%s%s/%s/change/%s' % info
            # admin_url = (
            #     u'<a href="%s" style="margin-left:10px;"><img src="%sadmin/img/admin/icon_changelink.gif" '
            #     u'width="10" height="10" alt="View current"/></a>'
            # ) % (url, settings.STATIC_URL)
            item = {
                'label_for': label_for,
                'rendered_cb': rendered_cb,
                'option_label': option_label,
                'option_value': option_value,
                'admin_url': admin_url,
            }

            if option_value in str_values:
                selected.append(item)
            else:
                unselected.append(item)

        # re-order `selected` array according str_values which is a set of `option_value`s in the order they should
        # be shown on screen
        ordered = []
        for value in str_values:
            for select in selected:
                if value == select['option_value']:
                    ordered.append(select)
        selected = ordered

        html = render_to_string(
            self.template,
            {'selected': selected, 'unselected': unselected})
        return mark_safe(html)
