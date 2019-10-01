# -*- coding: utf-8 -*-
from django import template
from django.core.cache import cache
from django.conf import settings

from filer.models import Folder
from easy_thumbnails.files import get_thumbnailer

from allink_core.core.loading import get_model
from allink_core.core.utils import get_height_from_ratio, get_ratio_w_h, get_key_from_dict

register = template.Library()

Config = get_model('config', 'Config')


# ####################################################################################
# Allink image

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
        # the outer most parent of all plugin with pictures should always be a content/column plugin
        # if not return a fallback of '1-of-1'. (potential_column gets None and will trow a AttributeError)
        try:
            # find the next column plugin
            column_plugin = None
            potential_column = plugin.parent.get_plugin_instance()[0]
            while (column_plugin is None):
                if potential_column.plugin_type == 'CMSAllinkContentColumnPlugin':
                    column_plugin = potential_column
                else:
                    potential_column = potential_column.parent.get_plugin_instance()[0]
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
            else:
                return '1-of-1'
        except AttributeError:
            return '2-of-3'

    # app plugin
    elif hasattr(plugin, 'items_per_row'):
        return '1-of-{}'.format(getattr(plugin, 'items_per_row', '1'))

    # template tag called from within an other context
    # this is a fallback, but should not come up if the correct width_alias is supplied in the template
    else:
        return '2-of-3'


def get_unique_key(context):
    if context.get('instance'):
        return context.get('instance').id
    else:
        return '{}-{}'.format(context.get('object').id, context.get('image').id)


@register.inclusion_tag('templatetags/allink_image.html', takes_context=True)
def render_image(context, image, alt_text='', ratio=None, width_alias=None, crop='smart', upscale=True, bw=False,
                 high_resolution=True, icon_enabled=True, bg_enabled=True, bg_color=None, lazyload_enabled=True,
                 zoom=None, subject_location=False, vh_enabled=False):
    """
    -> parameters:
    image: FilerImageField
    width_alias: '1-of-1'
    ratio: '3-2'

    -> optional parameters:
    alt_text: alternative image alt text
    crop: used for thumbnail gen
    bw: used for thumbnail gen
    icon_disabled: used in template
    bg_disabled: used in template
    bg_color: used in template
    zoom: used in template
    subject_location: used in template
    vh_enabled: used in template (using vh instead of percent)

    if you render a image from outside the content or app plugin content,
    it is important to supply a thumbnail width_alias
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

        # use focal point. works best in combination with zoom > 0
        if subject_location:
            subject_location = image.subject_location

        # update context
        context.update({'image': image})
        context.update({'icon_enabled': icon_enabled})
        context.update({'bg_enabled': bg_enabled})
        context.update({'bg_color': bg_color})
        context.update({'lazyload_enabled': lazyload_enabled})
        context.update({'alt_text': alt_text})
        context.update({'vh_enabled': vh_enabled})

        sizes = get_sizes_from_width_alias(width_alias)
        thumbnail_options = {'crop': crop, 'bw': bw, 'upscale': upscale, 'HIGH_RESOLUTION': high_resolution,
                             'zoom': zoom, 'subject_location': subject_location}

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
            context.update({'ratio_vh_{}'.format(size[0]): '{}vh'.format(h / w * 100)})
            context.update({'thumbnail_{}'.format(size[0]): thumbnailer.get_thumbnail(thumbnail_options)})
        # for css padding hack, a image in each ratio has to be unique
        # (break point doesnt matter, because is never shown at the same time)
        context.update({'picture_id': 'picture-{}'.format('-'.join((str(image.id), str(get_unique_key(context)),
                                                                    str(round(w)), str(round(h)))))})

    return context
