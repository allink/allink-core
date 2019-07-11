# -*- coding: utf-8 -*-
import ast
from django import template

from allink_core.apps.config.utils import get_page_meta_dict

register = template.Library()


@register.inclusion_tag('templatetags/allink_meta_og.html', takes_context=True)
def render_meta_og(context, obj=None, overwrite_dict=None):
    """
    e.g:
    {% render_meta_og %} or with an object {% render_meta_og news_entry %}

    :param context:
    default param for inclusion tag
    :param obj:
    an object which at least defines the required meta_ fields (defined in AllinkMetaTagMixin)
    :param overwrite_dict:
    you can overwrite or supply all the keys used in the template as a dict represented as string.
    e.g: {% render_meta_og overwrite_dict="{'meta_title': 'Hello', 'meta_description': 'Some Text',
    'meta_image_url':'www.foo.ch/image.jpg'}" %}
    Valid context variables are:
        meta_page_title
        meta_description
        google_site_verification
        meta_title
        meta_image_url
    :return:
    the updated context with all meta_ fields
    """

    meta_context = dict()
    if obj:
        meta_context = obj.meta_dict
    elif getattr(context.request, 'current_page', None):
        meta_context = get_page_meta_dict(getattr(context.request, 'current_page'))

    if overwrite_dict:
        overwrite_dict = ast.literal_eval(overwrite_dict)
        for key, value in overwrite_dict.items():
            meta_context[key] = value

    context.update(meta_context)
    return context
