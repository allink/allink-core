# -*- coding: utf-8 -*-s
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PageField
from adminsortable.fields import SortableForeignKey


# Page Chooser Plugin
class AllinkPageChooserPlugin(CMSPlugin):
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
    )

    def copy_relations(self, oldinstance):
        self.allinkpage_set.all().delete()

        for allink_page in oldinstance.allinkpage_set.all():
            allink_page.pk = None
            allink_page.pagechooser_id = self.id
            allink_page.save()

    class Meta:
        app_label = 'allink_cms'


# Page for Page Chooser
class AllinkPage(models.Model):
    pagechooser = SortableForeignKey(
        AllinkPageChooserPlugin,
        verbose_name=_(u'Images'),
        help_text=_(u'Add pages and order them.'),
        blank=True,
        null=True
    )
    just_descendants = models.BooleanField(
        _(u'Select just descendants'),
        help_text=_(
            u'If checked and pages selected manually, only the descendants of the selected pages will be listed.'),
        default=False
    )
    page = PageField()

    class Meta:
        app_label = 'allink_cms'
        verbose_name = _(u'Page')
        verbose_name_plural = _(u'Pages')

    def __str__(self):
        return str(self.page.get_menu_title())

# Language Chooser Plugin
class AllinkLanguageChooserPlugin(CMSPlugin):
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
    )

    class Meta:
        app_label = 'allink_cms'
