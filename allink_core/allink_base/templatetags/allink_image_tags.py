# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
from allink_core.allink_base.utils import get_height_from_ratio
register = template.Library()

# ####################################################################################
# Allink image

def get_percent(full, value):
    """
    returns a value in percent. (how much percent of ..)
    rounded whole numbers
    """
    return round(value * (100 / full))

def get_ratio_w_h(ratio):
    """
    returns width and height from string e.g. '1-2' or '4-3' as integer
    """
    w, h = ratio.split('-')
    return int(w), int(h)


def get_sizes_from_width_alias(width_alias):
    sizes = []
    aliases = settings.THUMBNAIL_WIDTH_ALIASES
    for point in aliases.get(width_alias):
        width = aliases.get(width_alias).get(point).get('width')
        ratio = aliases.get(width_alias).get(point).get('ratio')
        ratio_w, ratio_h = get_ratio_w_h(ratio)
        height = get_height_from_ratio(width, ratio_w, ratio_h)
        sizes.append((point, (width, height)))
    return sizes


def get_width_alias_from_plugin(context):
    plugin = context['instance']
    # plugin directly inside a column plugin
    if not hasattr(plugin, 'items_per_row'):
        # the parent of all plugin with pictures should always be a column plugin
        # if not return a fallback of '1-of-1'
        column_plugin = plugin.parent.djangocms_content_allinkcontentcolumnplugin
        if hasattr(column_plugin, 'template'):
            if column_plugin.template == 'col-1':
                return '1-of-1'
            elif column_plugin.template == 'col-1-1':
                return '1-of-2'
            elif column_plugin.template == 'col-1-2':
                return '1-of-3' if column_plugin.position == 0 else '2-of-3'
            elif column_plugin.template == 'col-2-1':
                return '2-of-3' if column_plugin.position == 0 else '1-of-3'
            elif column_plugin.template == 'col-3':
                return '1-of-3'
            elif column_plugin.template == 'col-4':
                return '1-of-4'
            elif column_plugin.template == 'col-5':
                return '1-of-5'
            elif column_plugin.template == 'col-6':
                return '1-of-6'
        else:
            return '1-of-1'

    # app plugin
    elif hasattr(plugin, 'items_per_row'):
        return '1-of-{}'.format(getattr(plugin, 'items_per_row', '1'))

    # template tag called from within an other context
    # this is a fallback, but should not come up if the correct width_alias is supplied in the template
    else:
        return '1-of-1'


def get_thumbnail(thumbnailer, thumbnail_options):
    """
    if no image was found, return a fallback image_not_found.jpg (if one was uploaded to Media Library)
    """
    try:
        return thumbnailer.get_thumbnail(thumbnail_options)
    except InvalidImageFormatError:
        from filer.models import Folder
        try:
            files = Folder.objects.get(name='Wireframe').files
        except Folder.DoesNotExist:
            return None
        for file in files:
            if file.original_filename.startswith('image-not-found'):
                try:
                    return get_thumbnailer(file).get_thumbnail(thumbnail_options)
                except InvalidImageFormatError:
                    return None
            return None
    except:
        return None


@register.inclusion_tag('templatetags/image.html', takes_context=True)
def render_image(context, image, ratio=None, width_alias=None, crop='smart', upscale=True, bw=False, high_resolution=True, icon_enabled=True, bg_enabled=True, bg_color=None):
    """
    -> parameters:
    image: FilerImageField
    width_alias: '1-of-1'
    ratio: '3-2'

    -> optional parameters:
    crop: used for thumbnail gen
    bw: used for thumbnail gen
    icon_disabled: used in template
    bg_disabled: used in template
    bg_color: used in template

    if you render a image from outside the content or app plugin content, it is important to supply a thumbnail width_alias
    otherwise the thumbnail will be rendered with the default width_alias '1-of-1' which might be to big.

    -> makes following context variable available in the template
    image (original image)
    thumbnail_url_xs
    thumbnail_url_md
    thumbnail_url_xl
    icon_disabled
    bg_disabled
    bg_color

    """
    if image:
        # explicit render image in this width_alias
        # most likely not from within an app plugin template or a content template
        if not width_alias:
            # get with alias from context
            width_alias = get_width_alias_from_plugin(context)

        # # respect the focal point set in the filer media gallery
        # if image.subject_location:
        #     focal_x, focal_y = image.subject_location.split(",")
        #     crop_x = get_percent(image.width, int(focal_x))
        #     crop_y = get_percent(image.height, int(focal_y))
        #     crop = '{},{}'.format(crop_x, crop_y)

        # update context
        context.update({'image': image})
        context.update({'icon_enabled': icon_enabled})
        context.update({'bg_enabled': bg_enabled})
        context.update({'bg_color': bg_color})

        sizes = get_sizes_from_width_alias(width_alias)
        thumbnail_options = {'crop': crop, 'bw': bw, 'upscale': upscale, 'HIGH_RESOLUTION': high_resolution}

        # create a thumbnail for each size
        for size in sizes:
            thumbnailer = get_thumbnailer(image)

            # override the default ratio or use THUMBNAIL_WIDTH_ALIASES ratio
            if ratio:
                w = size[1][0]
                # original ratio
                if ratio == 'x-y':
                    h = get_height_from_ratio(w, image.width, image.height)
                else:
                    ratio_w, ratio_h = get_ratio_w_h(ratio)
                    h = get_height_from_ratio(w, ratio_w, ratio_h)
            else:
                w, h = size[1][0], size[1][1]

            thumbnail_options.update({'size': (w, h)})
            context.update({'ratio_percent_{}'.format(size[0]): '{}%'.format(h / w * 100)})
            context.update({'thumbnail_{}'.format(size[0]): get_thumbnail(thumbnailer, thumbnail_options)})

        # for css padding hack, a image in each ratio has to be unique
        # (break point doesnt matter, because is never shown at the same time)
        context.update({'picture_id': 'picture-{}'.format('-'.join((str(image.id), str(round(w)), str(round(h)))))})

    return context

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
