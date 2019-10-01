# -*- coding: utf-8 -*-
import datetime
from django.db import models

from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PageField
from parler.models import TranslatableModel, TranslatedFields
from djangocms_text_ckeditor.fields import HTMLField

from allink_core.core.models import AllinkTimeFramedModel
from allink_core.core_apps.allink_terms.managers import AllinkTermsManager


class AllinkTerms(AllinkTimeFramedModel, TranslatableModel):

    STATUS_DRAFT = 10
    STATUS_PUBLISHED = 20
    STATUS_ARCHIVED = 30

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived'),
    )

    translations = TranslatedFields(
        text=HTMLField(
            'Terms Text'
        ),
    )

    terms_cms_page = PageField(
        verbose_name='Terms cms Page',
        null=True,
        on_delete=models.PROTECT,
        help_text='CMS Page which shows Terms and Conditions',
    )

    status = models.IntegerField('Status', choices=STATUS_CHOICES, default=STATUS_DRAFT)

    objects = AllinkTermsManager()

    class Meta:
        verbose_name = 'Terms of Service'
        verbose_name_plural = 'Terms of Service'
        app_label = 'allink_terms'

    def __str__(self):
        return 'Terms - %s' % self.get_status_display()

    def text_rendered(self):
        return self.text

    text_rendered.allow_tags = True

    @property
    def is_publishable(self):
        return self.status == AllinkTerms.STATUS_DRAFT

    def publish(self):
        self.save()
        now = datetime.datetime.now()

        try:
            curr_pub = AllinkTerms.objects.get_published()
            curr_pub.status = AllinkTerms.STATUS_ARCHIVED
            curr_pub.end = now
            curr_pub.save()
        except AllinkTerms.DoesNotExist:
            pass  # pass on first publication

        self.status = AllinkTerms.STATUS_PUBLISHED
        self.start = now
        self.save()

    def delete(self, *args, **kwargs):
        if self.status != AllinkTerms.STATUS_DRAFT:
            return  # can't delete models that already have been published
        return super(AllinkTerms, self).delete(*args, **kwargs)


class AllinkTermsPlugin(CMSPlugin):

    class Meta:
        app_label = 'allink_terms'

    def __str__(self):
        return str(self.pk)
