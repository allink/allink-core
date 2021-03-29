# -*- coding: utf-8 -*-
import re
from os.path import splitext
from django.db.models import Q
from allink_core.core.constants import STOP_WORDS_RE
from django.conf import settings
from django.utils.text import get_valid_filename as get_valid_filename_django
from django.template.defaultfilters import slugify

_base_url = None


def base_url():
    from django.contrib.sites.models import Site
    global _base_url
    if not '_base_url' not in locals() or not _base_url:
        scheme = 'http://' if settings.STAGE == 'local' else 'https://'
        _base_url = scheme + Site.objects.get_current().domain
    return _base_url


def get_additional_templates(model_name):
    """
    Get additional templates choices from settings for model_name
    """
    config = '{}_PLUGIN_TEMPLATES'.format(model_name.upper())
    additional_templates = getattr(settings, config, ())
    return additional_templates


def get_project_css_classes(model_name):
    """
    Get css_classes defined in settings for model_name
    """
    config = '{}_CSS_CLASSES'.format(model_name.upper())
    project_css_classes = getattr(settings, config, ())
    return project_css_classes


def get_additional_choices(config, blank=False):
    """
    Get additional settings var for project specific configuration
    """
    from allink_core.core.models.choices import BLANK_CHOICE
    choices = ()
    if blank:
        choices = BLANK_CHOICE
    choices += getattr(settings, config, ())
    return choices


def get_project_color_choices():
    """
    returns all projects specific colors
    """
    return getattr(settings, 'PROJECT_COLORS', {})


def get_ratio_choices():
    """
    returns all projects specific ratio choices
    """
    from allink_core.core.models.choices import BLANK_CHOICE, RATIO_CHOICES
    return BLANK_CHOICE + RATIO_CHOICES + get_additional_choices('RATIO_CHOICES')


def get_ratio_choices_orig():
    """
    returns all projects specific ratio choices
    including a 'original', which keeps the one from the file itself
    """
    from allink_core.core.models.choices import BLANK_CHOICE, RATIO_CHOICES_ORIG
    return BLANK_CHOICE + RATIO_CHOICES_ORIG + get_additional_choices('RATIO_CHOICES')


def get_image_width_alias_choices():
    """
    returns all projects specific ratio choices
    including a 'original', which keeps the one from the file itself
    """
    from allink_core.core.models.choices import BLANK_CHOICE, IMAGE_WIDTH_ALIAS_CHOICES
    image_width_alias_choices = get_additional_choices('IMAGE_WIDTH_ALIAS_CHOICES')
    if image_width_alias_choices:
        return BLANK_CHOICE + IMAGE_WIDTH_ALIAS_CHOICES + image_width_alias_choices
    return None


def get_height_from_ratio(width, ratio_w, ratio_h):
    """
    Used to calculate thumbnail height from given width and ratio
    """
    return width * ratio_h / ratio_w


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
    return float(w), float(h)


def get_display(key, list):
    """ returns key from list of tuples """
    d = dict(list)
    try:
        return d.get(int(key))
    except KeyError:
        return None


def replace_line_breaks(string):
    """replaces: '\r\n' and '\n\r' and '\r' and '\n' and with '<br />' """
    r = '<br />'
    return string.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)


def get_valid_filename(s):
    """
    like the regular get_valid_filename, but also slugifies away umlauts and
    stuff. Copied from django-filer
    """
    s = get_valid_filename_django(s)
    filename, ext = splitext(s)
    filename = slugify(filename)
    ext = slugify(ext)
    if ext:
        return "%s.%s" % (filename, ext)
    else:
        return "%s" % (filename,)


def normalize_query(query_string):
    """
    Split the query string into individual keywords, getting rid of unecessary
    spaces and grouping quoted words together.
    """
    find_terms = re.compile(r'"([^"]+)"|(\S+)').findall
    normalize_space = re.compile(r'\s{2,}').sub

    # Split the string into terms.
    terms = find_terms(query_string)

    # Only send unquoted terms through the stop words filter.
    for index, term in enumerate(terms):
        if term[1] != '':
            # If the term is a stop word, delete it from the list.
            if STOP_WORDS_RE.sub('', term[1]) == '':
                del terms[index]

    return [normalize_space(' ', (t[0] or t[1]).strip()) for t in terms]


def get_query(query_string, search_fields):
    """Return a query which is a combination of Q objects."""
    query = None
    terms = normalize_query(query_string)

    for term in terms:
        or_query = None

        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q

        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query


def get_key_from_dict(dict, value):
    """Takes a dict and a value, returns a list with matching keys."""
    try:
        return list(dict.keys())[list(dict.values()).index(value)]
    except ValueError:
        return None


def get_all_fields_from_form(instance):
    """"
    Return names of all available fields from given Form instance.

    :arg instance: Form instance
    :returns list of field names
    :rtype: list
    """

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields


def update_context_google_tag_manager(context, page_name='NOPAGE_NAME', page_id='NOPAGE_ID', plugin_id='NOPLUGIN_ID',
                                      name='NONAME'):
    """
    form_name = '{}{}_{}_{}'.format(page_name, page_id, plugin_id, name)
    If we have a form we will compile a id like this id="Kontakt88_plugin7451_SupportView"
    If its a Button Link we will try to compile it like  this id="Kontakt88_plugin7451_Support-Formular"
    If the Button Link Plugin is inside a static placeholder we will use the placeholder.slot and id instead of
    page infos
    """
    form_name = '{}{}_plugin{}_{}'.format(page_name, page_id, plugin_id, name)
    form_name = form_name.replace(' ', '-')
    context.update({'form_name': form_name})
    return context


def camelcase_to_separated_lowercase(string, separator):
    """
    :returns a lowercased strings separated by character a from an camelcased input string.
    e.g separator "-": 'AllinkTeaserGridContainerPlugin'-> 'allink-teaser-grid-container-plugin'
    """
    return re.sub(r'(?<!^)(?=[A-Z])', separator, string).lower()
