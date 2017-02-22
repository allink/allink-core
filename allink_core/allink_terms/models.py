# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeFramedModel
from parler.models import TranslatableModel, TranslatedFields
from djangocms_text_ckeditor.fields import HTMLField

from allink_core.allink_base.models import AllinkBaseModel

from .managers import AllinkTermsManager


class AllinkTerms(TranslatableModel, TimeFramedModel):

    STATUS_DRAFT = 10
    STATUS_PUBLISHED = 20
    STATUS_ARCHIVED = 30

    STATUS_CHOICES = (
        (STATUS_DRAFT, _(u'Draft')),
        (STATUS_PUBLISHED, _(u'Published')),
        (STATUS_ARCHIVED, _(u'Archived')),
    )

    translations = TranslatedFields(
        text=HTMLField(
            _(u'Terms Text')
        ),
    )

    status = models.IntegerField(_(u'Status'), choices=STATUS_CHOICES, default=STATUS_DRAFT)

    objects = AllinkTermsManager()

    class Meta:
        verbose_name = _(u'Terms of Service')
        verbose_name_plural = _(u'Terms of Service')

    def __unicode__(self):
        return _(u'Terms - %s') % self.get_status_display()

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
