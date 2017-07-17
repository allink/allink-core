# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin
from django.contrib.postgres.fields import ArrayField

from allink_core.core.models.choices import SOCIAL_ICONS_CHOICES


@python_2_unicode_compatible
class AllinkSocialIconContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for Social Icons
    """

    project_css_classes = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True
        ),
        blank=True,
        null=True
    )

    def __str__(self):
        return _(u'{}').format(str(self.pk))

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return ' '.join(css_classes)


@python_2_unicode_compatible
class AllinkSocialIconPlugin(CMSPlugin):
    title = models.CharField(
        _(u'Title'),
        help_text=_(u'SEO text (not visible) e.g. Follow allink on Instagram'),
        max_length=255,
        blank=True,
        null=True
    )
    icon = models.CharField(
        _(u'Icon'),
        max_length=50,
        choices=SOCIAL_ICONS_CHOICES
    )
    link = models.URLField(
        _(u'Link')
    )

    def __str__(self):
        return u'{}'.format(self.icon)
