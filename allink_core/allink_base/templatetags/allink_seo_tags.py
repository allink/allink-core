# -*- coding: utf-8 -*-
import hashlib

from django import template
from django.core.cache import cache

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
    cachekey = 'meta_og_%s' % hashlib.md5(str('%s_%s_%s_%s_%s_%s_%s' % (obj.__class__ if obj else '', obj.id if obj else '', page_title, base_page_title, image, og_title, description)).encode('utf-8')).hexdigest()
    cached_context = cache.get(cachekey, None)
    if cached_context is not None:
        context.update(cached_context)
        return context

    allink_config = AllinkConfig.get_solo()
    site = getattr(context.request, 'site')

    #  we pass a object when app content
    if obj:

        # base title
        if obj and obj.disable_base_title:
            base = ''
        else:
            if base_page_title:
                base = ' | ' + base_page_title
            elif getattr(allink_config, 'default_base_title', ''):
                base = ' | ' + getattr(allink_config, 'default_base_title', '')
            else:
                base = ' | ' + site.name

        # page title (<title>)
        if page_title:
            page_title += base
        elif obj.og_title:
            page_title = obj.og_title + base
        elif obj.title:
            page_title = obj.title + base
        else:
            page_title = getattr(allink_config, 'default_base_title', '')

        # title (for og:title)
        if og_title:
            og_title = og_title
        elif obj.og_title:
            og_title = obj.og_title
        elif obj.title:
            og_title = obj.title
        else:
            og_title = getattr(allink_config, 'default_base_title', '')

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
            try:
                image_url = allink_config.default_og_image.url
            except:
                image_url = None

    # cms page (no object is supplied)
    elif hasattr(context.request, 'current_page'):
        page = getattr(context.request, 'current_page')
        try:
            # only when extension is there
            page_ext = page.get_title_obj().allinkmetatagextension
        except:
            page_ext = None

        # base title
        if page_ext and page_ext.disable_base_title:
            base = ''
        else:
            if base_page_title:
                base = ' | ' + base_page_title
            elif getattr(allink_config, 'default_base_title', ''):
                base = ' | ' + getattr(allink_config, 'default_base_title', '')
            else:
                base = ' | ' + site.name


        # page title (<title>)
        if page_title:
            page_title += base
        elif page and page.get_page_title():
            page_title = page.get_page_title() + base
        else:
            page_title = getattr(allink_config, 'default_base_title', '')

        # og:title
        if og_title:
            og_title = og_title
        elif page and page.get_page_title():
            og_title = page.get_page_title()
        else:
            og_title = getattr(allink_config, 'default_base_title', '')

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
            try:
                image_url = page_ext.og_image.url if page_ext.og_image else allink_config.default_og_image.url
            except:
                image_url = None
        else:
            try:
                image_url = allink_config.default_og_image.url
            except:
                image_url = None

    additional_context = {
        'page_title': page_title,
        'og_title': og_title,
        'description': description,
        'image_url': image_url,
        'google_site_verification': allink_config.google_site_verification,
    }
    context.update(additional_context)
    cache.set(cachekey, additional_context, 60 * 5)
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
