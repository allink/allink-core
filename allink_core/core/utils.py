# -*- coding: utf-8 -*-
import re

from django.db.models import Q
from allink_core.core.constants import STOP_WORDS_RE
from django.conf import settings


_base_url = None


def base_url():
    from django.contrib.sites.models import Site
    global _base_url
    if not '_base_url' not in locals() or not _base_url:
        _base_url = 'https://' + Site.objects.get_current().domain
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
    return int(w), int(h)


def get_display(key, list):
    """ returns key from list of tuples """
    d = dict(list)
    try:
        return d.get(int(key))
    except:
        return None


def replace_line_breaks(string):
    """replaces: '\r\n' and '\n\r' and '\r' and '\n' and with '<br />' """
    r = '<br />'
    return string.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)


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
        if term[1] is not '':
            # If the term is a stop word, delete it from the list.
            if STOP_WORDS_RE.sub('', term[1]) is '':
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