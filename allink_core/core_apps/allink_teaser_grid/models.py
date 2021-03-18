# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from cms.models.pluginmodel import CMSPlugin
from django.contrib.postgres.fields import ArrayField


class AllinkTeaserGridContainerPlugin(CMSPlugin):
    TEMPLATES = (
        ('1-of-1', 'One Column'),
        ('1-of-2', 'Two Columns'),
        ('1-of-3', 'Three Columns'),
        ('1-of-4', 'Four Columns'),
    )

    COLUMN_ORDERS = (
        ('default', 'Default'),
        ('inverted', 'Inverted'),
        ('alternating', 'Alternating'),
    )

    SECTION_CSS_CLASSES = (
        ('custom-container-width-1', 'Reduce container width (8/12 cols)'),
        ('custom-container-width-2', 'Reduce container width (10/12 cols)'),
        ('container-fullwidth', 'Expand media (images/videos/galleries) width by 2 cols and expand to full-width on mobile.'),
    )

    SECTION_CSS_CLASSES_INITIAL = (
        'custom-container-width-1',
        'custom-container-width-2',
    )

    title = models.CharField(
        'Title',
        max_length=255,
        blank=True,
        null=True,
    )

    template = models.CharField(
        'Template',
        help_text='Choose a template.',
        max_length=50,
        choices=TEMPLATES,
        default=TEMPLATES[0],
    )

    column_order = models.CharField(
        'Column Order',
        help_text='Choose a column order.',
        max_length=50,
        choices=COLUMN_ORDERS,
        default=COLUMN_ORDERS[0],
    )

    anchor = models.CharField(
        verbose_name='ID',
        max_length=255,
        blank=True,
        help_text=('ID of this content section which can be used for anchor reference from links.<br>'
                   'Note: Only letters, numbers and hyphen. No spaces or special chars.'),
    )

    project_css_classes = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True
        ),
        blank=True,
        null=True
    )

    project_css_spacings_top_bottom = models.CharField(
        'Spacings',
        help_text='Choose a spacing (top and bottom).',
        max_length=50,
        blank=True,
        null=True,
    )

    project_css_spacings_top = models.CharField(
        'Spacings top',
        help_text='Choose a top spacing.',
        max_length=50,
        blank=True,
        null=True,
    )

    project_css_spacings_bottom = models.CharField(
        'Spacings bottom',
        help_text='Choose a bottom spacing.',
        max_length=50,
        blank=True,
        null=True,
    )

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)

        return ' '.join(css_classes)

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
