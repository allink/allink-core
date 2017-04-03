# -*- coding: utf-8 -*-
from functools import partial
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils import translation
from django.utils.translation import ugettext as _
from django.core.urlresolvers import NoReverseMatch

from cms.models.pluginmodel import CMSPlugin

from treebeard.mp_tree import MP_Node

from importlib import import_module

from allink_core.allink_base.forms import fields


# Add an app namespace to related_name to avoid field name clashes
# with any other plugins that have a field with the same name as the
# lowercase of the class name of this model.
# https://github.com/divio/django-cms/issues/5030
CMSPluginField = partial(
    models.OneToOneField,
    to=CMSPlugin,
    related_name='%(app_label)s_%(class)s',
    parent_link=True,
)


class Classes(models.TextField):
    default_field_class = fields.Classes
    south_field_class = 'django.db.models.fields.TextField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Css Classes')
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        if 'help_text' not in kwargs:
            kwargs['help_text'] = _('Space separated classes that are added to '
                                    'the list of classes.')
        super(Classes, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Classes, self).formfield(**defaults)


class Icon(models.CharField):
    default_field_class = fields.Icon
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Icon')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Icon, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Icon, self).formfield(**defaults)


class ZipCodeField(PositiveIntegerField):
    default_validators = [MaxValueValidator(9999)]
    default_field_class = fields.ZipCode
    description = _("Zip Code Field")

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(ZipCodeField, self).formfield(**defaults)


def choices_from_sitemaps():
    '''
        Helper for SitemapField
        Build up select choices
        from items declared in sitemaps
        - If we got a MPTT object (https://github.com/django-mptt/django-mptt)
        display indentation according to level
        - Display page language where we can get to it
        - Handle i18n sitemaps correctly
    '''
    try:
        from django.conf import settings
        url_mod = import_module(settings.ROOT_URLCONF)
        sitemaps = url_mod.sitemaps
    # TODO: specify ErrorType
    except:
        sitemaps = {}

    def label_from_instance(instance, lang=None):
        if hasattr(instance, '_mptt_meta'):
            # we got a tree object
            level = getattr(instance, instance._mptt_meta.level_attr)
        elif isinstance(instance, MP_Node):
            # we got a tree object from treebeard
            level = instance.depth - 1
        else:
            # fallback, no different levels
            level = 0

        name = instance.__unicode__()
        if level:
            level_indicator = '---' * level
            name = u'%s %s' % (level_indicator, name)

        if lang:
            name = u'%s (%s)' % (name, lang)
        elif hasattr(instance, 'language'):
            name = u'%s (%s)' % (name, getattr(instance, 'language'))
        return name

    def get_sitemap_urls(item, sitemap):
        # copied from django.contrib.sitemaps.get_urls()
        # cycle trough all languages for i18n sensitive
        # sitemaps
        if getattr(sitemap, 'i18n', False):
            out = []
            current_lang_code = translation.get_language()
            for lang_code, lang_name in settings.LANGUAGES:
                translation.activate(lang_code)
                try:
                    out += [(item.get_absolute_url(), label_from_instance(item, lang=lang_code))]
                except AttributeError:
                    try:
                        out += [(item.page.get_absolute_url(), label_from_instance(item.page, lang=lang_code))]
                    except AttributeError:
                        # Entry does not exist in this language
                        pass
                    except NoReverseMatch:
                        # get_absolute_url does not work for this element
                        pass
                except NoReverseMatch:
                    # get_absolute_url does not work for this element
                    pass
            translation.activate(current_lang_code)
        else:
            out = []
            try:
                out = [(item.get_absolute_url(), label_from_instance(item))]
            except AttributeError:
                try:
                    out = [(item.page.get_absolute_url(), label_from_instance(item.page))]
                except NoReverseMatch:
                    # get_absolute_url does not work for this element
                    pass
            except NoReverseMatch:
                # get_absolute_url does not work for this element
                pass
        return out

    urls = [(None, '----------')]
    for name, sitemap in sitemaps.iteritems():
        if callable(sitemap):
            urls += [(None, '')]
            urls += [(None, name.upper())]
            urls += [(None, '----------')]
            sitemap = sitemap()
            for item in sitemap.items():
                urls += get_sitemap_urls(item, sitemap)
    return urls


class SitemapField(models.TextField):
    """
    This field collects all entries from Sitemaps,
    and Maps them back on model instances. Like this
    you can give a choice from all URLs which are listed
    in sitemaps in a user-readable way.
    """

    choices = []

    def __init__(self, *args, **kwargs):
        super(SitemapField, self).__init__(*args, **kwargs)
        # self.choices = choices_from_sitemaps()
