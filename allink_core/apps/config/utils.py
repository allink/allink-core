# -*- coding: utf-8 -*-
import operator
import types
from django.conf import settings
from cms.models.pagemodel import Page
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError

from allink_core.apps.config.constants import PAGE_FIELD_FALLBACK_CONF
from allink_core.core.loading import get_model

Config = get_model('config', 'Config')
AllinkPageExtension = get_model('config', 'AllinkPageExtension')
AllinkTitleExtension = get_model('config', 'AllinkTitleExtension')


def get_page_meta_dict(page):
    """
    Function which returns all relevant meta fields of a CMSPage. (Defines the fallback hierarchy.)
    Is the Page equivalent of AllinkMetaTagMixin.

    Used in combination with:
    AllinkPageExtension
    AllinkTitleExtension
    """
    allink_config = Config.get_solo()
    meta_context = {
        'meta_page_title': get_meta_page_title(page),
        'meta_title': get_fallback(page, 'meta_title'),
        'meta_description': get_fallback(page, 'meta_description'),
        'meta_image_url': getattr(get_meta_page_image_thumb(page), 'url', ''),
        'google_site_verification': allink_config.google_site_verification,
    }
    return meta_context


def get_meta_page_title(page):
    allink_config = Config.get_solo()
    base_title = ' | ' + getattr(allink_config, 'default_base_title', '')
    page_title = get_fallback(page, 'meta_title')

    return page_title + base_title


def get_meta_page_image_thumb(page):
    """
    :param page:
    cms page object
    :return
    a thumbnail image object
    """
    meta_image = get_fallback(page, 'meta_image')
    return generate_meta_image_thumb(meta_image)


def get_page_teaser_dict(page):
    """
    Function which returns all relevant teaser fields of a CMSPage. (Defines the fallback hierarchy.)
    Is the Page equivalent of AllinkTeaserMixin.

    Used in combination with:
    AllinkPageExtension
    AllinkTitleExtension
    """
    meta_context = {
        'teaser_title': get_fallback(page, 'teaser_title'),
        'teaser_technical_title': get_fallback(page, 'teaser_technical_title'),
        'teaser_description': get_fallback(page, 'teaser_description'),
        'teaser_image': get_fallback(page, 'teaser_image'),
        'teaser_link_text': get_fallback(page, 'teaser_link_text'),
        'teaser_link': page.get_absolute_url(),
    }
    return meta_context


def get_fallback(obj, field_name):
    """
    returns the fallback value of a predefined field for a property (e.g 'meta_image' or 'teaser_title')

    This is either used for CMS Page objects or objects which implement a 'field_fallback_conf' property.

    :param obj:
    either a CMS Page object or an object which subclasses  ...
    :param field_name:
    the key in the .._FIELD_FALLBACK_CONF dict
    :return:
    the value of the fallback field or None (it's your responsibility to handle None values in the template or in a
    _dict mapper method e.g meta_dict or teaser_dict)
    """

    if isinstance(obj, Page):
        conf = PAGE_FIELD_FALLBACK_CONF.get(field_name, list())
        obj_mapper = {
            'self': obj,
            'cms.Title': obj.get_title_obj(),
            'config.Config': get_model('config', 'Config').get_solo(),
            'settings': settings,
        }
    else:
        conf = obj.field_fallback_conf.get(field_name, list())
        obj_mapper = {
            'self': obj,
            'config.Config': get_model('config', 'Config').get_solo(),
            'settings': settings,
        }

    for field_dict in conf:
        model = field_dict.get('model')
        field_lookup = field_dict.get('field')

        obj = obj_mapper.get(model)

        try:
            attr = operator.attrgetter(field_lookup)(obj)
            if attr:
                if isinstance(attr, types.MethodType) and attr():
                    return attr()
                else:
                    return attr
        except AttributeError:
            continue
    else:
        # if there is no fallback listed in ..FALLBACK_CONF for this field, try to return the attribute directly
        getattr(obj, field_name, None)


def generate_meta_image_thumb(meta_image):
    """
    We always want the meta image with a maximum width of 1200px and a height of 630px.
    This is what Facebook recommends. As for other platforms this might not be the best ratio.

    :param meta_image:
    an filer image object
    :return
    a thumbnail image object
    """

    if not meta_image:
        return None

    width = 1200
    height = 630

    thumbnail_options = {'crop': 'smart', 'upscale': True, 'HIGH_RESOLUTION': False,
                         'subject_location': meta_image.subject_location, 'size': (width, height)}

    try:
        thumbnailer = get_thumbnailer(meta_image)
        thumbnail = thumbnailer.get_thumbnail(thumbnail_options)
    except InvalidImageFormatError:
        thumbnail = None
    return thumbnail
