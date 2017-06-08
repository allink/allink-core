# -*- coding: utf-8 -*-
from django import template
from cms.models.pagemodel import Page
from allink_core.allink_config.models import AllinkConfig
register = template.Library()

####################################################################################
# Meta and og: > renders all meta and og:tags

@register.inclusion_tag('templatetags/allink_meta_og.html', takes_context=True)
def render_meta_og(context, obj=None, page_title=None, base_page_title=None, image=None, og_title=None, description=None):
    """
    either pass all variables with this tag explicitly 
    or get it from either the page 
    or the app content (then supply the object)
    """

    allink_config = AllinkConfig.get_solo()
    site = getattr(context.request, 'site')

    #  we pass a object when app content
    if obj:
        # page title
        if page_title:
            page_title = page_title
        elif obj.title:
            page_title = obj.title
        else:
            page_title = allink_config.default_base_title

        if base_page_title:
            page_title += ' | ' + base_page_title
        elif not obj.enable_base_title:
            page_title = page_title
        elif allink_config.default_base_title:
            page_title += ' | ' + allink_config.default_base_title
        else:
            page_title += ' | ' + site.name

        # title
        if og_title:
            og_title = og_title
        elif obj.og_title:
            og_title = obj.og_title
        else:
            og_title = obj.title

        # description
        if description:
            description = description
        elif obj.og_description:
            description = obj.og_description
        elif obj.lead:
            description = obj.lead
        else:
            description = ''

        # image
        if image:
            image_url = image.url
        elif obj.og_image:
            image_url = obj.og_image.url
        elif obj.preview_image:
            image_url = obj.preview_image.url
        else:
            image_url = allink_config.default_og_image.url

    # cms page (no object is supplied)
    elif hasattr(context.request, 'current_page'):
        page = getattr(context.request, 'current_page')
        try:
            # only when extension is there
            page_ext = page.get_title_obj().allinkmetatagextension
        except:
            page_ext = None

        # page title
        if page_title:
            page_title = page_title
        elif page.get_page_title():
            page_title = page.get_page_title()
        else:
            page_title = allink_config.default_base_title

        if base_page_title:
            page_title += ' | ' + base_page_title
        elif page_ext and not page_ext.enable_base_title:
            page_title = page_title
        elif allink_config.default_base_title:
            page_title += ' | ' + allink_config.default_base_title
        else:
            page_title += ' | ' + site.name

        # title
        if og_title:
            og_title = og_title
        elif page:
            og_title = page.get_page_title()
        else:
            # for example django admin page
            og_title = ''

        # description
        if description:
            description = description
        elif page:
            description = page.get_meta_description()
        else:
            # for example django admin page
            description = ''

        # image
        if image:
            image_url = image.url
        elif page_ext and page_ext.og_image:
            image_url = page_ext.og_image.url if page_ext.og_image else allink_config.default_og_image.url
        else:
            image_url = allink_config.default_og_image.url


    context.update({
        'page_title': page_title,
        'og_title': og_title,
        'description': description,
        'image_url': image_url,
        'google_site_verification': allink_config.google_site_verification,
    })

    return context


####################################################################################
# page h1: > renders h1 tag

@register.inclusion_tag('templatetags/allink_h1.html', takes_context=True)
def render_h1(context, obj=None, text=None):
    site = getattr(context.request, 'site')

    if text:
        text = text
    #  we pass a object when app content
    elif obj:
        text = obj.title
    # cms page (no object is supplied)
    elif hasattr(context.request, 'current_page'):
        page = getattr(context.request, 'current_page')
        try:
            # only when extension is there
            page_ext = page.get_title_obj().allinkmetatagextension
        except:
            page_ext = None

        if page_ext and page_ext.override_h1:
            text = page_ext.override_h1
        elif page and page.get_page_title():
            text = page.get_page_title()
        # for example django admin page
        else:
            text = site.name
    else:
        text = site.name

    context.update({
            'text': text,
        })

    return context
