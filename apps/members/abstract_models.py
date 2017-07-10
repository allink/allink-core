# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from parler.models import TranslatableModel, TranslatedField, TranslatedFieldsModel
from model_utils.models import TimeStampedModel
from aldryn_translation_tools.models import TranslationHelperMixin

from allink_core.core.loading import get_model
from allink_core.core_apps.allink_mailchimp.config import MailChimpConfig
from allink_core.core_apps.allink_mailchimp.helpers import list_members_delete, list_members_put, get_status_if_new
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin

config = MailChimpConfig()


@python_2_unicode_compatible
class BaseMembers(TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, TimeStampedModel):
    slug_source_field_name = 'full_name'

    slug = TranslatedField(any_language=True)

    member_nr = models.CharField(
        _(u'Member Number'),
        max_length=30,
        unique=True,
        blank=False
    )

    email = models.EmailField(
        _(u'Email'),
    )

    first_name = models.CharField(
        _(u'First Name'),
        max_length=30,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        _(u'Last Name'),
        max_length=30,
        blank=True
    )

    language = models.CharField(
        _(u'Language'),
        max_length=3,
        default=settings.LANGUAGE_CODE
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        app_label = 'members'
        verbose_name = _('Members')
        verbose_name_plural = _('Members')

    def __str__(self):
        return u'{}: {} {}'.format(self.member_nr, self.user.first_name, self.user.last_name)

    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @classmethod
    def get_verbose_name(cls):
        Config = get_model('config', 'Config')
        try:
            field_name = cls._meta.model_name + '_verbose'
            return getattr(Config.get_solo(), field_name)
        except:
            return cls._meta.verbose_name

    @classmethod
    def get_verbose_name_plural(cls):
        Config = get_model('config', 'Config')
        try:
            field_name = cls._meta.model_name + '_verbose_plural'
            return getattr(Config.get_solo(), field_name)
        except:
            return cls._meta.verbose_name_plural

    def save(self, **kwargs):
        if not self.pk:
            user, created = User.objects.get_or_create(
                username=self.member_nr,
                email=self.email,
                # password=settings.MEMBERS_INITIAL_PWD,
                first_name=self.first_name,
                last_name=self.last_name
            )
            group = Group.objects.get_or_create(name='Mitglieder')
            user.groups.add(group[0])
            self.language = get_language()
            self.user = user
            # self.put_to_mailchimp_list()
        else:
            self.user.username = self.member_nr
            self.user.email = self.email
            self.user.last_name = self.last_name
            self.user.first_name = self.first_name
            self.user.save()
        super(BaseMembers, self).save(**kwargs)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
            self.delete_from_mailchimp_list()
        super(BaseMembers, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        app = '{}:detail'.format(self._meta.model_name)
        return reverse(app, kwargs={'slug': self.slug})

    def log(self, log, description):
        MembersLog = get_model('members', 'MembersLog')
        MembersLog.objects.create(members=self, log=log, description=description)

    def put_to_mailchimp_list(self, member_hash_email=None):
        data = {
            'email_address': self.email,
            'status': 'subscribed',
            'status_if_new': get_status_if_new(),
            'language': self.language,
            'merge_fields': {
                'FNAME': self.first_name,
                'LNAME': self.last_name
            }
        }
        if config.merge_vars:
            data = data.append(config.merge_vars)

        list_members_put(data=data, member_hash_email=member_hash_email)

    def delete_from_mailchimp_list(self):
        data = {
            'email_address': self.email,
        }
        if config.merge_vars:
            data = data.append(config.merge_vars)
        list_members_delete(data)


class BaseMembersTranslation(TranslatedFieldsModel):
    master = models.ForeignKey('members.Members', related_name='translations', null=True)

    slug = models.SlugField(
        _(u'Slug'),
        max_length=255,
        default='',
        blank=True,
        help_text=_(u'Leave blank to auto-generate a unique slug.')
    )
    class Meta:
        abstract = True
        app_label = 'members'


@python_2_unicode_compatible
class BaseMembersLog(models.Model):
    log = models.CharField(
        _(u'Log'),
        max_length=255
    )

    description = models.CharField(
        _(u'Description'),
        max_length=255
    )

    members = models.ForeignKey('members.Members')

    created = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        abstract = True
        app_label = 'members'
        ordering = ('-created',)

    def __str__(self):
        return self.log
