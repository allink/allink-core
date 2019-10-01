# -*- coding: utf-8 -*-s
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PageField
from adminsortable.fields import SortableForeignKey
from allink_core.core.models.fields import CMSPluginField


class AllinkPageChooserPlugin(CMSPlugin):
    cmsplugin_ptr = CMSPluginField()

    def copy_relations(self, oldinstance):
        self.allinkpage_set.all().delete()

        for allink_page in oldinstance.allinkpage_set.all():
            allink_page.pk = None
            allink_page.pagechooser_id = self.id
            allink_page.save()

    class Meta:
        app_label = 'allink_cms'


class AllinkPage(models.Model):
    pagechooser = SortableForeignKey(
        AllinkPageChooserPlugin,
        verbose_name='Images',
        on_delete=models.SET_NULL,
        help_text='Add pages and order them.',
        blank=True,
        null=True
    )
    just_descendants = models.BooleanField(
        'Select just descendants',
        help_text=_(
            'If checked and pages selected manually, only the descendants of the selected pages will be listed.'),
        default=False
    )
    page = PageField()

    class Meta:
        app_label = 'allink_cms'
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return str(self.page.get_menu_title())


class AllinkLanguageChooserPlugin(CMSPlugin):
    cmsplugin_ptr = CMSPluginField()

    class Meta:
        app_label = 'allink_cms'
