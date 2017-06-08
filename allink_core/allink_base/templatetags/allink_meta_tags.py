# -*- coding: utf-8 -*-
from django import template
from cms.models.pagemodel import Page
from allink_core.allink_config.models import AllinkConfig
register = template.Library()

####################################################################################
# Meta and og: > renders all meta and og:tags

@register.inclusion_tag('templatetags/allink_meta_og.html', takes_context=True)
def render_meta_og(context, obj=None, image=None, og_title=None, description=None):
    """
    either pass all variables with this tag explicitly 
    or get it from either the page 
    or the app content (then supply the object)
    """

    allink_config = AllinkConfig.get_solo()

    #  we pass a object when app contnet
    if obj:
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
        else:
            description = obj.lead

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

        # title
        if og_title:
            og_title = og_title
        elif page_ext:
            og_title = page_ext.og_title if page_ext.og_title else page.get_page_title()
        elif page:
            og_title = page.get_page_title()
        else:
            # for example django admin page
            og_title = ''

        # description
        if description:
            description = description
        elif page_ext and page_ext.og_description:
            description = page_ext.og_description if page_ext.og_description else page.get_meta_description()
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
        'og_title': og_title,
        'description': description,
        'image_url': image_url,
        'google_site_verification': allink_config.google_site_verification,
    })

    return context
