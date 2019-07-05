# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from django.contrib.postgres.fields import ArrayField


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
        return _('{}').format(str(self.pk))

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return ' '.join(css_classes)


class AllinkSocialIconPlugin(CMSPlugin):
    title = models.CharField(
        _('Title'),
        help_text=_('SEO text (not visible) e.g. Follow allink on Instagram'),
        max_length=255,
        blank=True,
        null=True
    )
    icon = models.CharField(
        _('Icon'),
        max_length=50
    )
    link = models.URLField(
        _('Link')
    )

    def __str__(self):
        return u'{}'.format(self.icon)
