# -*- coding: utf-8 -*-

from django.db import models
from cms.models.pluginmodel import CMSPlugin


class AllinkTeaserGridContainerPlugin(CMSPlugin):
    title = models.CharField(
        'Title',
        max_length=255,
        blank=True,
        null=True,
    )

    project_css_spacings_top_bottom = models.CharField(
        'Spacings',
        help_text='Choose a spacing (top and bottom).',
        max_length=50,
        blank=True,
        null=True
    )
    project_css_spacings_top = models.CharField(
        'Spacings top',
        help_text='Choose a top spacing.',
        max_length=50,
        blank=True,
        null=True
    )
    project_css_spacings_bottom = models.CharField(
        'Spacings bottom',
        help_text='Choose a bottom spacing.',
        max_length=50,
        blank=True,
        null=True
    )

    @property
    def css_section_classes(self):
        css_classes = []
        if self.project_css_spacings_top:
            css_classes.append('{}-top'.format(self.project_css_spacings_top))

        if self.project_css_spacings_bottom:
            css_classes.append('{}-bottom'.format(self.project_css_spacings_bottom))

        if self.project_css_spacings_top_bottom:
            css_classes = self.project_css_spacings_top_bottom
            return css_classes

        return ' '.join(css_classes)

    def __str__(self):
        return str(self.id)
