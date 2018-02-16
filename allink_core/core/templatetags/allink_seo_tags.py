# -*- coding: utf-8 -*-
import hashlib

from django import template
from django.core.cache import cache
from django.utils.html import strip_tags

from allink_core.core.loading import get_model

register = template.Library()

Config = get_model('config', 'Config')

####################################################################################
# Meta and og: > renders all meta and og:tags

def get_page_title(allink_config, disable_base, title_prio_1, title_prio_2, title_prio_3, base_prio_1, base_prio_2):
    page_title_full = ''
    # base title
    if disable_base:
        base = ''
    else:
        if base_prio_1:
            base = ' | ' + base_prio_1
        elif getattr(allink_config, 'default_base_title'):
            base = ' | ' + getattr(allink_config, 'default_base_title', '')
        else:
            base = ' | ' + base_prio_2

    # page title (<title>)
    if title_prio_1:
        page_title_full = page_title_full + base
    elif title_prio_2:
        page_title_full = title_prio_2 + base
    elif title_prio_3:
        page_title_full = title_prio_3 + base
    else:
        page_title_full = getattr(allink_config, 'default_base_title', '')

    return page_title_full


def get_og_title(allink_config, prio_1, prio_2, prio_3):
    # title (for og:title)
    if prio_1:
        og_title = prio_1
    elif prio_2:
        og_title = prio_2
    elif prio_3:
        og_title = prio_3
    else:
        og_title = getattr(allink_config, 'default_base_title', '')
    return og_title


def get_description(prio_1, prio_2, prio_3):
    if prio_1:
        description = prio_1
    elif prio_2:
        description = prio_2
    elif prio_3:
        description = prio_3
    else:
        description = ''
    return description


def get_image_url(allink_config, prio_1, prio_2, prio_3):
    if prio_1:
        image_url = prio_1.url
    elif prio_2:
        image_url = prio_2.url
    elif prio_3:
        image_url = prio_3.url
    else:
        try:
            image_url = allink_config.default_og_image.url
        except AttributeError:
            image_url = ''
    return image_url


@register.inclusion_tag('templatetags/allink_meta_og.html', takes_context=True)
def render_meta_og(context, obj=None, page_title=None, base_page_title=None, image=None, og_title=None, description=None):
    """
    either pass all variables with this tag explicitly
    or get it from either the page
    or the app content (then supply the object)
    """

    allink_config = Config.get_solo()
    site = getattr(context.request, 'site')

    #  we pass a object when app content
    if obj:

        page_title_final = get_page_title(
            allink_config,
            obj.disable_base_title,
            page_title,
            obj.og_title,
            obj.title,
            base_page_title,
            site.name
        )

        og_title = get_og_title(allink_config, og_title, obj.og_title, obj.title)
        description = get_description(description, obj.og_description, strip_tags(getattr(obj, 'lead', '')))
        image_url = get_image_url(allink_config, image, getattr(obj, 'og_image'), getattr(obj, 'preview_image'))

    # cms page (no object is supplied)
    elif hasattr(context.request, 'current_page'):
        page = getattr(context.request, 'current_page')
        # is it a cms page (or is it a non)
        if page:
            cms_page_title = page.get_page_title()
            cms_meta_descr = page.get_meta_description()
        else:
            cms_page_title = None
            cms_meta_descr = None

        try:
            # only when extension is there (cms page must not have a extension)
            page_ext = page.get_title_obj().allinkmetatagextension
            page_ext_og_image = getattr(page_ext, 'og_image')
        except:
            page_ext = None
            page_ext_og_image = None

        page_title_final = get_page_title(
            allink_config,
            getattr(page_ext, 'disable_base_title', False),
            page_title,
            cms_page_title,
            None,
            base_page_title,
            site.name
        )

        og_title = get_og_title(allink_config, og_title, cms_page_title, None)
        description = get_description(description, cms_meta_descr, None)
        image_url = get_image_url(allink_config, image, page_ext_og_image, None)


    additional_context = {
        'page_title': page_title_final,
        'og_title': og_title,
        'description': description,
        'image_url': image_url,
        'google_site_verification': allink_config.google_site_verification,
    }
    context.update(additional_context)

    return context


@register.inclusion_tag('templatetags/allink_softpage_title.html', takes_context=True)
def render_softpage_title(context, obj=None, page_title=None, base_page_title=None):
    """
    either pass all variables with this tag explicitly
    or get it from either the page
    or the app content (then supply the object)
    """

    allink_config = Config.get_solo()
    site = getattr(context.request, 'site')

    #  we pass a object when app content
    if obj:

        page_title_final = get_page_title(
            allink_config,
            obj.disable_base_title,
            page_title,
            obj.og_title,
            obj.title,
            base_page_title,
            site.name
        )

    # cms page (no object is supplied)
    elif hasattr(context.request, 'current_page'):
        page = getattr(context.request, 'current_page')
        # is it a cms page (or is it a non)
        if page:
            cms_page_title = page.get_page_title()
        else:
            cms_page_title = None
        try:
            # only when extension is there (cms page must not have a extension)
            page_ext = page.get_title_obj().allinkmetatagextension
        except:
            page_ext = None

        page_title_final = get_page_title(
            allink_config,
            getattr(page_ext, 'disable_base_title', False),
            page_title,
            cms_page_title,
            None,
            base_page_title,
            site.name
        )

    additional_context = {
        'page_title': page_title_final,
    }
    context.update(additional_context)

    return context


####################################################################################
# page h1: > renders h1 tag

@register.inclusion_tag('templatetags/allink_h1.html', takes_context=True)
def render_h1(context, obj=None, text=None):
    if hasattr(context, 'request'):
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
                page_ext = page.get_title_obj().allinkseoextension
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
    else:
        if text:
            text = text
        #  we pass a object when app content
        elif obj:
            text = obj.title
        # cms page (no object is supplied)
        else:
            text = ''

    context.update({
        'text': text,
    })

    return context
