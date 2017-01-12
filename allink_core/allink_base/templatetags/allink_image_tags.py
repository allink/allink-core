# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('templatetags/app_content_image.html', takes_context=True)
def render_app_content_image_detail(context,thumbnail_url):

    # add different BREAKPOINT and RETINA suffixes
    thumbnail_url_xs = thumbnail_url+'-xs'
    thumbnail_url_xs_2x = thumbnail_url_xs+'-2x'
    thumbnail_url_sm = thumbnail_url+'-sm'
    thumbnail_url_sm_2x = thumbnail_url_sm+'-2x'
    thumbnail_url_xl = thumbnail_url+'-xl'
    thumbnail_url_xl_2x = thumbnail_url_xl+'-2x'

    # update context
    context.update({'thumbnail_url_xs': thumbnail_url_xs})
    context.update({'thumbnail_url_xs_2x': thumbnail_url_xs_2x})
    context.update({'thumbnail_url_sm': thumbnail_url_sm})
    context.update({'thumbnail_url_sm_2x': thumbnail_url_sm_2x})
    context.update({'thumbnail_url_xl': thumbnail_url_xl})
    context.update({'thumbnail_url_xl_2x': thumbnail_url_xl_2x})

    return context

@register.inclusion_tag('templatetags/app_content_image.html', takes_context=True)
def render_app_content_image(context,thumbnail_url=None):

    # Define variable base according to template
    if not thumbnail_url:
        thumbnail_url = 'col-{}'.format(context['instance'].items_per_row) if context['instance'].items_per_row else 'col-2'

    # add different BREAKPOINT and RETINA suffixes
    thumbnail_url_xs = thumbnail_url+'-xs'
    thumbnail_url_xs_2x = thumbnail_url_xs+'-2x'
    thumbnail_url_sm = thumbnail_url+'-sm'
    thumbnail_url_sm_2x = thumbnail_url_sm+'-2x'
    thumbnail_url_xl = thumbnail_url+'-xl'
    thumbnail_url_xl_2x = thumbnail_url_xl+'-2x'

    # update context
    context.update({'thumbnail_url_xs': thumbnail_url_xs})
    context.update({'thumbnail_url_xs_2x': thumbnail_url_xs_2x})
    context.update({'thumbnail_url_sm': thumbnail_url_sm})
    context.update({'thumbnail_url_sm_2x': thumbnail_url_sm_2x})
    context.update({'thumbnail_url_xl': thumbnail_url_xl})
    context.update({'thumbnail_url_xl_2x': thumbnail_url_xl_2x})

    return context


@register.inclusion_tag('templatetags/allink_image.html', takes_context=True)
def render_content_image(context):

    column_plugin = context['instance'].parent.djangocms_content_allinkcontentcolumnplugin

    # Define variable base according to template
    thumbnail_url = ''
    if column_plugin.template == 'col-1':
        thumbnail_url = 'col-3-of-3'
    elif column_plugin.template == 'col-1-1':
        thumbnail_url = 'col-1-of-2'
    elif column_plugin.template == 'col-1-2':
        thumbnail_url = 'col-1-of-3' if column_plugin.position == 0 else 'col-2-of-3'
    elif column_plugin.template == 'col-2-1':
        thumbnail_url = 'col-2-of-3' if column_plugin.position == 0 else 'col-1-of-3'
    elif column_plugin.template == 'col-3':
        thumbnail_url = 'col-1-of-3'

    # add different BREAKPOINT and RETINA suffixes
    thumbnail_url_xs = thumbnail_url+'-xs'
    thumbnail_url_xs_2x = thumbnail_url_xs+'-2x'
    thumbnail_url_sm = thumbnail_url+'-sm'
    thumbnail_url_sm_2x = thumbnail_url_sm+'-2x'
    thumbnail_url_xl = thumbnail_url+'-xl'
    thumbnail_url_xl_2x = thumbnail_url_xl+'-2x'

    # update context
    context.update({'thumbnail_url_xs': thumbnail_url_xs})
    context.update({'thumbnail_url_xs_2x': thumbnail_url_xs_2x})
    context.update({'thumbnail_url_sm': thumbnail_url_sm})
    context.update({'thumbnail_url_sm_2x': thumbnail_url_sm_2x})
    context.update({'thumbnail_url_xl': thumbnail_url_xl})
    context.update({'thumbnail_url_xl_2x': thumbnail_url_xl_2x})

    return context
