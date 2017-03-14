# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin

from allink_core.allink_base.utils import get_additional_templates


@python_2_unicode_compatible
class AllinkInstagramPlugin(CMSPlugin):
    """
    A plugin representing an Instagram Feed
    """

    GRID_STATIC = 'grid_static'

    TEMPLATES = (
        (GRID_STATIC, 'Grid (Static)'),
    )

    # COLUMN AMOUNT
    COLUMN_AMOUNT = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
    )

    # ORDERING
    DEFAULT = 'default'
    RANDOM = 'random'
    LATEST = 'latest'

    ORDERING = (
        (DEFAULT, '---------'),
        (LATEST, 'latest first'),
        (RANDOM, 'random'),
    )

    title = models.CharField(
        _(u'Title'),
        help_text=_(u'The section title'),
        max_length=255,
        blank=True,
        null=True
    )
    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50,
        choices=TEMPLATES,
        default=TEMPLATES[0]
    )
    ordering = models.CharField(
        _(u'Sort order'),
        help_text=_(u'Choose a order.'),
        max_length=50,
        choices=ORDERING,
        default=ORDERING[0]
    )
    items_per_row = models.IntegerField(
        _(u'Grid items per row'),
        help_text=_(u'Only applied if a "Grid" template has been selected.'),
        choices=COLUMN_AMOUNT,
        default=3
    )
    paginated_by = models.IntegerField(
        _(u'Max. entries per page'),
        default=9,
        help_text=_(u'Set to 0 if all entries should be displayed on first page.')
    )
    account = models.CharField(
        _(u'Account'),
        help_text=_(u'Instagram account name'),
        max_length=255,
    )
    follow_text = models.CharField(
        _(u'Follow Text'),
        help_text=_(u'Follow us text i.e.: Tag your images with #awesomehashtag'),
        max_length=255,
        blank=True,
        null=True
    )

    def get_templates(self):
        for x, y in get_additional_templates(self._meta.model_name):
            self.TEMPLATES += ((x, y),)
        return self.TEMPLATES

    def __str__(self):
        if self.title and self.template:
            return u'{} ({})'.format(self.title, self.template)
        elif self.template:
            return u'({})'.format(self.template)
        return str(self.pk)
