# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

# ####################################################################################
# # in a template

# {% example_image_tag width_alias="1-of-2" ratio="2-1" %}


# ####################################################################################
# # settings.py

# THUMBNAIL_WIDTH_ALIAS = {
#     '1-of-2': {'xs':450,'md': 1200, 'lg': 1500},
#     '1-of-3': {'xs':450,'md': 500, 'lg': 600},
#     ...
# }

# DEFAULT_IMAGE_RATIOS = (
#     ('1-of-2','3-2'),
#     ('1-of-3','3-2'),
#     ...
# )

# ####################################################################################
# # utility function

# def get_default_image_ratio_from_width_alias(width_alias):
#     # find width_alias and return ratio from DEFAULT_IMAGE_RATIOS
#     return ratio

# def generate_thumbnail_sizes(thumbnailer,width_alias,ratio):

#     # http://easy-thumbnails.readthedocs.io/en/2.1/usage/#python
#     thumbnail_options.update({'size': (size, size)})
#     thumbnail_xs = thumbnailer.get_thumbnail(thumbnail_options)

#     # thumbnail_dimensions = {
#     #     {'thumbnail_xs': thumbnail_xs},
#     #     {'thumbnail_xs_2x': thumbnail_xs_2x},
#     #     {'thumbnail_sm': thumbnail_sm},
#     #     {'thumbnail_sm_2x': thumbnail_sm_2x},
#     #     {'thumbnail_lg': thumbnail_lg},
#     #     {'thumbnail_lg_2x': thumbnail_lg_2x},
#     # }
#     return thumbnail_dimensions

####################################################################################
# templatetag

# from easy_thumbnails.files import get_thumbnailer
# from settings import THUMBNAIL_WIDTH_ALIAS

# @register.inclusion_tag('templatetags/allink_image_2.html', takes_context=True)
# def example_image_tag(context, width_alias=None, ratio=None, icon_disabled=False, bg_disabled=False, bg_color=None, bw=False, crop='smart'):

#     # create thumbnailer instance of image object
#     thumbnailer = get_thumbnailer(the_image)

#     # thumbnail options
#     thumbnail_options = {'crop': crop}
#     if bw:
#         thumbnail_options.update({'bw': True})

#     # No "width_alias" according to context, if no "width_alias" is set
#     if not width_alias:

#         # Case 1. Content Plugin > Column?
#         if column_plugin
#             # Get ratio
#             ratio = context.ratio
#             # Determine "width_alias" depending on which COLUMN we're in.
#             if column_plugin.template == 'col-1-1':
#                 width_alias = '1-of-2'
#                 # ...

#         # Case 2. App Plugin -> Determine "width_alias" depending on number of GRID COLUMNS
#         elif context['instance'].items_per_row:
#             width_alias = '1-of-{}'.format(context['instance'].items_per_row) if context['instance'].items_per_row else '1-of-2'

#     # At this stage, we have e.g. width_alias="1-of-2"

#     # If no "ratio" is set, fall back to defaeult
#     if not ratio:
#         # get info according to "width_alias" in DEFAULT_IMAGE_RATIOS
#         # not
#         ratio = get_default_image_ratio_from_width_alias(width_alias)

#     # And then.. Create thumbnail FOR EACH SIZE and store variables in CONTEXT so we can use in the TEMPLATE
#     context.update(generate_thumbnail_sizes(thumbnailer,width_alias,ratio));

#     return context

####################################################################################
# Allink specific image


@register.inclusion_tag('templatetags/allink_specific_image.html', takes_context=True)
def render_allink_image(context, image, thumbnail_url):

    # add different BREAKPOINT and RETINA suffixes
    thumbnail_url_xs = thumbnail_url + '-xs'
    thumbnail_url_xs_2x = thumbnail_url_xs + '-2x'
    thumbnail_url_sm = thumbnail_url + '-sm'
    thumbnail_url_sm_2x = thumbnail_url_sm + '-2x'
    thumbnail_url_xl = thumbnail_url + '-xl'
    thumbnail_url_xl_2x = thumbnail_url_xl + '-2x'

    # update context
    context.update({'thumbnail_url_xs': thumbnail_url_xs})
    context.update({'thumbnail_url_xs_2x': thumbnail_url_xs_2x})
    context.update({'thumbnail_url_sm': thumbnail_url_sm})
    context.update({'thumbnail_url_sm_2x': thumbnail_url_sm_2x})
    context.update({'thumbnail_url_xl': thumbnail_url_xl})
    context.update({'thumbnail_url_xl_2x': thumbnail_url_xl_2x})

    context.update({'object': image})

    return context

####################################################################################
# App Content Plugin > Detail view


@register.inclusion_tag('templatetags/app_content_image.html', takes_context=True)
def render_app_content_image_detail(context, thumbnail_url, icon_disabled=False, bg_disabled=False, bg_color=0):

    # add different BREAKPOINT and RETINA suffixes
    thumbnail_url_xs = thumbnail_url + '-xs'
    thumbnail_url_xs_2x = thumbnail_url_xs + '-2x'
    thumbnail_url_sm = thumbnail_url + '-sm'
    thumbnail_url_sm_2x = thumbnail_url_sm + '-2x'
    thumbnail_url_xl = thumbnail_url + '-xl'
    thumbnail_url_xl_2x = thumbnail_url_xl + '-2x'

    # update context
    context.update({'thumbnail_url_xs': thumbnail_url_xs})
    context.update({'thumbnail_url_xs_2x': thumbnail_url_xs_2x})
    context.update({'thumbnail_url_sm': thumbnail_url_sm})
    context.update({'thumbnail_url_sm_2x': thumbnail_url_sm_2x})
    context.update({'thumbnail_url_xl': thumbnail_url_xl})
    context.update({'thumbnail_url_xl_2x': thumbnail_url_xl_2x})

    # variations
    context.update({'bg_color': bg_color})
    context.update({'icon_disabled': icon_disabled})
    context.update({'bg_disabled': bg_disabled})

    return context

####################################################################################
# App Content Plugin > List view


@register.inclusion_tag('templatetags/app_content_image.html', takes_context=True)
def render_app_content_image(context, thumbnail_url=None, icon_disabled=False, bg_disabled=False, bg_color=0):

    # Define variable base according to template
    if not thumbnail_url:
        thumbnail_url = 'col-{}'.format(context['instance'].items_per_row) if context['instance'].items_per_row else 'col-2'

    # add different BREAKPOINT and RETINA suffixes
    thumbnail_url_xs = thumbnail_url + '-xs'
    thumbnail_url_xs_2x = thumbnail_url_xs + '-2x'
    thumbnail_url_sm = thumbnail_url + '-sm'
    thumbnail_url_sm_2x = thumbnail_url_sm + '-2x'
    thumbnail_url_xl = thumbnail_url + '-xl'
    thumbnail_url_xl_2x = thumbnail_url_xl + '-2x'

    # update context
    context.update({'thumbnail_url_xs': thumbnail_url_xs})
    context.update({'thumbnail_url_xs_2x': thumbnail_url_xs_2x})
    context.update({'thumbnail_url_sm': thumbnail_url_sm})
    context.update({'thumbnail_url_sm_2x': thumbnail_url_sm_2x})
    context.update({'thumbnail_url_xl': thumbnail_url_xl})
    context.update({'thumbnail_url_xl_2x': thumbnail_url_xl_2x})

    # variations
    context.update({'bg_color': bg_color})
    context.update({'icon_disabled': icon_disabled})
    context.update({'bg_disabled': bg_disabled})

    return context


####################################################################################
# Content Plugin > Images placed in columns

@register.inclusion_tag('templatetags/allink_image.html', takes_context=True)
def render_content_image(context, thumbnail_url=None, icon_disabled=False, bg_disabled=False, icon_enabled=True, bg_enabled=True):

    column_plugin = context['instance'].parent.djangocms_content_allinkcontentcolumnplugin

    # Define variable base according to template
    if not thumbnail_url:
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
        elif column_plugin.template == 'col-4':
            thumbnail_url = 'col-1-of-4'
        elif column_plugin.template == 'col-5':
            thumbnail_url = 'col-1-of-5'
        elif column_plugin.template == 'col-6':
            thumbnail_url = 'col-1-of-6'
            icon_disabled = True
            bg_disabled = True
        # fallback for additional templtaes in settings.py
        else:
            thumbnail_url = 'col-1'

    # add different BREAKPOINT and RETINA suffixes
    thumbnail_url_xs = thumbnail_url + '-xs'
    thumbnail_url_xs_2x = thumbnail_url_xs + '-2x'
    thumbnail_url_sm = thumbnail_url + '-sm'
    thumbnail_url_sm_2x = thumbnail_url_sm + '-2x'
    thumbnail_url_xl = thumbnail_url + '-xl'
    thumbnail_url_xl_2x = thumbnail_url_xl + '-2x'

    # update context
    context.update({'thumbnail_url_xs': thumbnail_url_xs})
    context.update({'thumbnail_url_xs_2x': thumbnail_url_xs_2x})
    context.update({'thumbnail_url_sm': thumbnail_url_sm})
    context.update({'thumbnail_url_sm_2x': thumbnail_url_sm_2x})
    context.update({'thumbnail_url_xl': thumbnail_url_xl})
    context.update({'thumbnail_url_xl_2x': thumbnail_url_xl_2x})

    # lazyloader definitions
    if not icon_enabled:
        icon_disabled = True

    if not bg_enabled:
        bg_disabled = True

    context.update({'icon_disabled': icon_disabled})
    context.update({'bg_disabled': bg_disabled})

    return context


####################################################################################
# Favicons > renders all favicons in folder "favicons"

@register.inclusion_tag('templatetags/allink_favicon_set.html', takes_context=True)
def render_favicons_set(context):
    from filer.models import Folder
    from django.contrib import messages
    from allink_core.allink_config.models import AllinkConfig

    apple_favs = []
    android_favs = []
    favicons = []

    try:
        files = Folder.objects.get(name='favicons').files
    except Folder.DoesNotExist:
        messages.warning(context.request, _(u'Please create a folder "favicons" and upload the complete favicon set.'))
        return

    for file in files:
        if file.original_filename.startswith('apple-touch-icon'):
            apple_favs.append(file)
        elif file.original_filename.startswith('android-chrome'):
            android_favs.append(file)
        elif file.original_filename.startswith('favicon-'):
            favicons.append(file)
        elif file.original_filename.startswith('favicon.ico'):
            context.update({'favicon': file})
        elif file.original_filename.startswith('mstile'):
            context.update({'mstile': file})
        elif file.original_filename.startswith('safari-pinned-tab'):
            context.update({'mask_icon': file})

    context.update({
        'apple_favs': apple_favs,
        'android_favs': android_favs,
        'favicons': favicons,
        'allink_config': AllinkConfig.get_solo(),
    })

    return context
