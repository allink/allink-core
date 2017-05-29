# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import ugettext_lazy as _
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
            description = None

        description = obj.og_description if obj.og_description else None
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
        page_ext = page.get_title_obj().allinkmetatagextension

        # title
        #  % page_attribute page_title %}{% endif %}{% endblock og_title %} {% block og_title_base %}| {{ request.site.name }}{% endblock og_title_base %}
        if og_title:
            og_title = og_title
        elif page_ext.og_title:
            og_title = page_ext.og_title
        else:
            og_title = page.get_page_title()

        # description
        if description:
            description = description
        elif page_ext.og_description:
            description = page_ext.og_description
        else:
            description = page.get_meta_description()

        # image
        if image:
            image_url = image.url
        elif page_ext.og_image.url:
            image_url = page_ext.og_image.url

        else:
            image_url = allink_config.default_og_image.url


    context.update({
        'og_title': og_title,
        'description': description,
        'image_url': image_url,
        'google_site_verification': allink_config.google_site_verification,
    })

    return context
