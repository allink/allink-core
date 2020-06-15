# -*- coding: utf-8 -*-
from django import template
from cms.models import Page
from cms.templatetags.cms_tags import CMSEditableObject
from django.utils import translation

register = template.Library()


@register.simple_tag
def page_from_slug(slug):
    return Page.objects.get(slug=slug)


@register.simple_tag
def placeholder_has_content(placeholder):
    """
    Renders boolean to variable if placeholder has plugins or not in active language
    """

    return bool(placeholder.cmsplugin_set.filter(language=translation.get_language()))


class CMSEditableObjectAjax(CMSEditableObject):
    """
    Used to render correct title (with editable double click)
    """
    edit_template_ajax = 'templatetags/allink_plugin_ajax.html'

    def _is_ajax(self, request):
        return request.is_ajax()

    def get_template(self, context, **kwargs):
        if self._is_editable(context.get('request', None)):
            if self._is_ajax(context.get('request', None)):
                return self.edit_template_ajax
            else:
                return self.edit_template
        return self.template


register.tag('render_model_ajax', CMSEditableObjectAjax)
