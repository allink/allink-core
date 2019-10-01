# -*- coding: utf-8 -*-

from django.db import models
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
        return '{}'.format(str(self.pk))

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return ' '.join(css_classes)


class AllinkSocialIconPlugin(CMSPlugin):
    title = models.CharField(
        'Title',
        help_text='SEO text (not visible) e.g. Follow allink on Instagram',
        max_length=255,
        blank=True,
        null=True
    )
    icon = models.CharField(
        'Icon',
        max_length=50
    )
    link = models.URLField(
        'Link'
    )

    def __str__(self):
        return '{}'.format(self.icon)
