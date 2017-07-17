# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class AllinkGroupContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for Group of Content
    """

    title = models.CharField(
        _(u'Title'),
        max_length=255
    )

    groups = models.ManyToManyField(
        Group,
        blank=True,
    )

    def __str__(self):
        return self.title

    def copy_relations(self, oldinstance):
        self.groups = oldinstance.groups.all()


@python_2_unicode_compatible
class AllinkGroupPlugin(CMSPlugin):
    title = models.CharField(
        _(u'Title'),
        max_length=255
    )

    def __str__(self):
        return u'{}'.format(self.title)
