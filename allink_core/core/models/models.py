# -*- coding: utf-8 -*-
import urllib.parse
from urllib.parse import urlparse
import phonenumbers
from importlib import import_module

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, override
from django.utils.functional import cached_property
from cms.utils.i18n import get_current_language, get_default_language
from cms.models.pluginmodel import CMSPlugin

from parler.models import TranslatedFieldsModel
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from djangocms_attributes_field.fields import AttributesField
from cms.models.fields import PageField

from allink_core.core.utils import base_url, get_additional_templates
from allink_core.core.loading import get_model
from allink_core.core.models.managers import AllinkBaseModelManager
from allink_core.core.models.choices import SALUTATION_CHOICES, TARGET_CHOICES, NEW_WINDOW, SOFTPAGE_LARGE, SOFTPAGE_SMALL, FORM_MODAL, IMAGE_MODAL, DEFAULT_MODAL, BLANK_CHOICE
from allink_core.core.models.fields import ZipCodeField
from allink_core.core.models.mixins import AllinkInvalidatePlaceholderCacheMixin
from allink_core.core.utils import get_additional_choices
from allink_core.core_apps.allink_categories.models import AllinkCategory


@python_2_unicode_compatible
class AllinkBaseModel(AllinkInvalidatePlaceholderCacheMixin, models.Model):
    """
     An abstract base class model for every standard allink app

    """

    # Is used to auto generate Category
    category_name_field = u'title'

    ACTIVE = 1
    INACTIVE = 2

    STATUS_COICES = [
        (ACTIVE, _('active')),
        (INACTIVE, _('inactive'))
    ]

    created = AutoCreatedField(_('created'), editable=True)
    modified = AutoLastModifiedField(_('modified'))

    categories = models.ManyToManyField(
        AllinkCategory,
        blank=True
    )
    status = models.IntegerField(_('status'), choices=STATUS_COICES, default=ACTIVE)
    auto_generated_category = models.OneToOneField(
        AllinkCategory,
        related_name=u'auto_generated_from_%(class)s',
        null=True,
        blank=True,
    )
    og_image = FilerImageField(
        verbose_name=_(u'og:Image'),
        help_text=_(u'Preview image when page/post is shared on Facebook/ Twitter. <br>Min. 1200 x 630 for best results. If not set, the one from the preview image will be used, if not set or not in a app context, the one defined in allink_settings will be used.'),
        blank=True,
        null=True
    )
    disable_base_title = models.BooleanField(
        _(u'Disable base title'),
        help_text=_(u'If disabled, only the page title will be shown. Everything behind and including the "|" will be removed.'),
        default=False
    )
    objects = AllinkBaseModelManager()

    class Meta:
        abstract = True
        app_label = 'allinkbasemodel'

    def __str__(self):
        return u'%s - %s' % (self.title, self.created.strftime('%d.%m.%Y'))

    @classmethod
    def get_published(cls):
        return cls.objects.active()

    @classmethod
    def get_next(cls, instance):
        return cls.get_published().filter(created__gt=instance.created, id__gt=instance.id).order_by('created', 'id').first()

    @classmethod
    def get_previous(cls, instance):
        return cls.get_published().filter(created__lt=instance.created, id__lt=instance.id).order_by('created', 'id').last()

    @classmethod
    def get_relevant_categories(cls):
        """
        returns a queryset of all relevant categories for a the model_name
        """
        result = AllinkCategory.objects.none()
        for root in AllinkCategory.get_root_nodes().filter(model_names__contains=[cls._meta.model_name]):
            result |= root.get_descendants()
        return result

    @cached_property
    def next(self):
        return self.get_next(self)

    @cached_property
    def previous(self):
        return self.get_previous(self)

    @cached_property
    def fetch_categories(self):
        return self.categories.all()

    # deprecated
    @cached_property
    def show_detail_link(self):
        return True

    @classmethod
    def get_can_have_categories(cls):
        return cls._meta.model_name in dict(settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES)

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    @classmethod
    def get_verbose_name_plural(cls):
        return cls._meta.verbose_name_plural

    def is_published(self):
        return self in self.get_published()

    is_published.short_description = _(u'Published')
    is_published.boolean = True

    def get_detail_view(self, application_namespace=None):
        if application_namespace:
            return '{}:detail'.format(application_namespace)
        else:
            return '{}:detail'.format(self._meta.model_name)

    def get_absolute_url(self, language=None, application_namespace=None):
        from django.core.urlresolvers import reverse
        if not language:
            language = get_current_language() or get_default_language()

        slug, language = self.known_translation_getter(
            'slug', None, language_code=language)
        app = self.get_detail_view(application_namespace)
        try:
            with override(language):
                return reverse(app, kwargs={'slug': slug})
        except NoReverseMatch:
            return '/no_app_hook_configured'

    def get_full_url(self):
        return base_url() + self.get_absolute_url()

    def save_categories(self, new):
        """
        Some models are used as categories.
        For these we auto-generate a new category
        for each instance. The category gets
        ajusted in case of changes.

        new: boolean, telling if an instance is new or just changed
        """

        # getting translation class
        if new:
            # all categories generated from one model, should be in the same root category
            # if not existing, this root needs to be created too
            try:
                super_cat = AllinkCategory.objects.get(translations__name=self._meta.verbose_name)
            except AllinkCategory.DoesNotExist:
                super_cat = AllinkCategory.add_root()
                super_cat.name = self._meta.verbose_name
                super_cat.save()
            cat = super_cat.add_child(tag=self._meta.model_name)
        else:
            cat = self.auto_generated_category

        from parler.utils.context import switch_language

        # source model is translatable, so create all the appropriate translations
        if hasattr(self, 'translations') and self.translations.exists():
            for translation in self.translations.all():
                with switch_language(cat, translation.language_code):
                    # we have to special case locations because we have a subtitle which matters
                    if translation._meta.model_name == 'locationstranslation':
                        cat.name = '{} {}'.format(getattr(translation, self.category_name_field), getattr(translation, 'subtitle'))
                    else:
                        cat.name = getattr(translation, self.category_name_field)
                    # we also generates new slug no matter what
                    cat.slug = ''
                    cat.save()

        # and the source model isn't translatable
        else:
            if self._meta.model_name == 'locations':
                cat.name = '{} {}'.format(getattr(self, self.category_name_field),
                                          getattr(self, 'subtitle'))
            else:
                cat.name = getattr(self, self.category_name_field)
            # we also generates new slug no matter what
            cat.slug = ''
            cat.save()
        return cat

    def save(self, *args, **kwargs):
        new = not bool(self.id)
        if not new:
            self.save_translations(*args, **kwargs)
        if self._meta.model_name in dict(settings.PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES).keys():
            self.auto_generated_category = self.save_categories(new)
        super(AllinkBaseModel, self).save(*args, **kwargs)


@receiver(post_delete)
def post_delete_auto_generated_category(sender, instance, *args, **kwargs):
    if not issubclass(sender, AllinkBaseModel):
        return
    if instance.auto_generated_category:
        instance.auto_generated_category.delete()


@python_2_unicode_compatible
class AllinkBaseTranslatedFieldsModel(TranslatedFieldsModel):

    class Meta:
        abstract = True

    og_title = models.CharField(
        verbose_name=_(u'Title Tag and Title when shared on Facebook/ Twitter.'),
        max_length=255,
        help_text=_(u'Title when shared on Facebook.'),
        blank=True,
        null=True
    )
    og_description = models.CharField(
        verbose_name=_(u'Meta Description for Search Engines and when shared on Facebook.'),
        max_length=255,
        help_text=_(u'Description when shared on Facebook/ Twitter.'),
        blank=True,
        null=True
    )


@python_2_unicode_compatible
class AllinkBaseAppContentPlugin(CMSPlugin):
    """
    Base plugin which provides standard functionality
    all Content App-Plugins should inherit from this, to create a "app pointer plugin"

    - allows to display application content for different apps
    - ability to filter and sort entries
    - manually select entries (search entries and select/ sort)

    """

    data_model = None

    # PAGINATION
    NO = 'no'
    LOAD = 'load'
    LOAD_REST = 'load_rest'
    # PAGES = 'pages'

    PAGINATION_TYPE = (
        (NO, 'None'),
        (LOAD, 'Add "Load more"-Button'),
        (LOAD_REST, 'Add "Load all"-Button'),
        # (PAGES, 'Page Navigation'),
    )

    # COLUMN AMOUNT
    COLUMN_AMOUNT = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
    )

    # ORDERING
    DEFAULT = 'default'
    TITLE_ASC = 'title_asc'
    TITLE_DESC = 'title_desc'
    LATEST = 'latest'
    EARLIEST = 'earliest'
    RANDOM = 'random'
    CATEGORY = 'category'

    ORDERING = (
        (DEFAULT, '---------'),
        (TITLE_ASC, 'A-Z (title)'),
        (TITLE_DESC, 'Z-A (title'),
        (LATEST, 'latest first'),
        (EARLIEST, 'earliest first'),
        (RANDOM, 'random'),
        (CATEGORY, 'category ordering'),
    )

    FILTERING = (
        (DEFAULT, '---------'),
    )

    # FILTER FIELDS
    FILTER_FIELD_CHOICES = (
        # ('categories', {
        #     'verbose': _(u'Categories'),
        #     'query_filter': {},
        #     # example
        #     # 'query_filter': {'translations__name': 'Bern'},
        # }),
    )

    # FIELDS
    categories = models.ManyToManyField(
        AllinkCategory,
        blank=True
    )
    categories_and = models.ManyToManyField(
        AllinkCategory,
        blank=True,
        related_name='%(app_label)s_%(class)s_categories_and'
    )

    manual_filtering = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    manual_ordering = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    filter_fields = ArrayField(models.CharField(
        max_length=50),
        blank=True,
        null=True,
        default=None
    )

    # manual_entries  -> defined in subclasses (no elegant way found to define this here.)
    # apphook_page -> defined in subclasses (no elegant way found to define this here.)

    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50
    )
    category_navigation_enabled = models.BooleanField(
        _(u'Show category navigation'),
        help_text=_(u'If checked, a filter navigation with all selected categories is displayed.<br>Please note: A category is only displayed if it contains items.'),
        default=False
    )
    category_navigation_all = models.BooleanField(
        _(u'Show category "all"'),
        help_text=_(u'If checked, a category "all" in filter navigation is displayed.'),
        default=False
    )
    category_navigation = models.ManyToManyField(
        AllinkCategory,
        related_name='%(app_label)s_%(class)s_category_navigation',
        verbose_name=_(u'Categories for Navigation'),
        help_text=_(u'You can explicitly define the categories for the category navigation here. This will override the automatically set of categories (either the one generated from "Filter & Ordering" or "Manual entries")'),
        blank=True,
    )
    softpage_enabled = models.BooleanField(
        _(u'Show detailed information in Softpage'),
        help_text=_(u'If checked, the detail view of an entry will be displayed in a "softpage". Otherwise the page will be reloaded.'),
        default=True
    )
    detail_link_enabled = models.BooleanField(
        _(u'Show detail link'),
        help_text=_(u'If checked, a link/button to the detail view will be displayed.'),
        default=True
    )
    items_per_row = models.IntegerField(
        _(u'Grid items per row'),
        help_text=_(u'Only applied if a "Grid" template has been selected.'),
        choices=COLUMN_AMOUNT,
        default=3
    )
    paginated_by = models.IntegerField(
        _(u'Max. entries per page'),
        default=0,
        help_text=_(u'Limit the number of entries (in case of the "load more" pagination type: entries per page). Default is "0" (show all entries)')
    )
    pagination_type = models.CharField(
        _(u'Pagination Type'),
        max_length=50,
        choices=PAGINATION_TYPE,
        default=PAGINATION_TYPE[0]
    )
    load_more_button_text = models.CharField(
        _(u'Text for "Load .."-Button'),
        help_text=_(u'If left blank, a default text will be used. <br>Note: Should the default text be adjusted site-wide, please contact the project manager (such changes can be made on a code level)'),
        max_length=255,
        null=True,
        blank=True
    )
    detail_link_text = models.CharField(
        _(u'Text for "Detail"-Link'),
        help_text=_(u'If left blank, a default text will be used.<br>Note: Should the default text be adjusted site-wide, please contact the project manager (such changes can be made on a code level)'),
        max_length=255,
        null=True,
        blank=True
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
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    @classmethod
    def get_templates(cls):
        templates = ()
        for x, y in get_additional_templates(cls.data_model._meta.model_name):
            templates += ((x, y),)
        return templates

    @classmethod
    def get_filtering_choices(cls):
        return cls.FILTERING

    @classmethod
    def get_ordering_choices(cls):
        return cls.ORDERING

    @cached_property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        css_classes.append('{}-template'.format(self.template)) if self.template else None
        css_classes.append('items-per-row-{}'.format(self.items_per_row)) if self.items_per_row else None
        return ' '.join(css_classes)

    def copy_relations(self, oldinstance):
        self.categories = oldinstance.categories.all()
        self.categories_and = oldinstance.categories_and.all()
        self.category_navigation = oldinstance.category_navigation.all()
        self.manual_entries = oldinstance.manual_entries.all()

    def get_selected_entries(self, filters={}):
        queryset = self.fetch_manual_entries.filter(**filters)
        return self._get_queryset_with_prefetch_related(self._apply_ordering_to_queryset_for_display(queryset))

    def get_model_name(self):
        return self.data_model._meta.model_name

    def get_app_can_have_categories(self):
        if self.data_model._meta.model_name in dict(settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES):
            return True
        else:
            return False

    def get_correct_template(self, file):
        # file can only be '_items', 'content', 'no_results'
        if file != 'no_results':
            template = '{}/plugins/{}/{}.html'.format(self.data_model._meta.app_label, self.template, file)
        else:
            template = '{}/plugins/{}.html'.format(self.data_model._meta.app_label, file)
        return template

    def get_field_info(self, fieldname):
        """
        returns None if not foreignkey, otherswise the relevant model
        """
        from django.db.models import ForeignKey
        is_translated = False
        try:
            field_object, model, direct, m2m = self.data_model._meta.get_field_by_name(fieldname)
        # in case that the field is translated, it can't be found on the model itself
        # so we get the translationmodel and get all data from there.
        except FieldDoesNotExist:
            is_translated = True
            field_object, model, direct, m2m = self.data_model.translations.related.related_model._meta.get_field_by_name(fieldname)
        if (direct and isinstance(field_object, ForeignKey)) or (direct and m2m):
            return field_object.rel.to, is_translated
        return None, is_translated

    def get_distinct_values_of_field(self, fieldname):
        """
        returns distinct values_list for fieldname
        the query_filter defined in FILTER_FIELD_CHOICES gets applied here
        """
        try:
            query_filter = {u'%s__%s' % (fieldname, k): v for k, v in dict(self.FILTER_FIELD_CHOICES)[fieldname]['query_filter'].items()}
        except KeyError:
            query_filter = {}
        try:
            # order alphabetically if not 'categories' (they are ordered by 'lft')
            order_by = fieldname if fieldname != 'categories' else 'lft'
            return self.get_render_queryset_for_display().filter(**query_filter).order_by(order_by).values_list(fieldname).distinct()
        # handle translated fields
        except FieldError:
            translation_model = self.data_model.translations.related.related_model
            model_query = self.get_render_queryset_for_display().filter(**query_filter)
            return translation_model.objects.filter(language_code=get_current_language(), master__in=model_query).order_by(order_by).values_list(fieldname).distinct()

    def get_filter_fields_with_options(self):
        """
        returns dict with all filter fields and there distinct values of the particular model field
        (e.g. list of {categories: [(10, 'News')..], place: [2, 'Zürich']}
        TODO: at the moment only one value for "filter_fields" is supported. (makes "load more" logic simpler)
        """
        options = {}
        for fieldname in self.filter_fields:
            # field is foreignkey or m2m, so we have to get the verbose name form the model itself
            filters = [((None, _(u'All'),))]
            fk_model, is_translated = self.get_field_info(fieldname)
            if fk_model:
                filters.extend((entry.id, entry.__str__(),) for entry in
                               fk_model.objects.filter(
                                   id__in=self.get_distinct_values_of_field(fieldname)))
            # field is no foreignkey and no m2m
            else:
                filters.extend((urllib.parse.quote_plus(value[0]), value[0]) for value in self.get_distinct_values_of_field(fieldname))
            filter_key = "%s-translations__%s" % (self.data_model._meta.model_name, fieldname) if is_translated else "%s-%s" % (self.data_model._meta.model_name, fieldname)
            options.update({filter_key: (dict(self.FILTER_FIELD_CHOICES)[fieldname]['verbose'], filters)})
        return options

    @cached_property
    def fetch_categories(self):
        return self.categories.all()

    @cached_property
    def fetch_first_category(self):
        return self.categories.first()

    @cached_property
    def fetch_categories_and(self):
        return self.categories_and.all()

    @cached_property
    def fetch_manual_entries(self):
        return self.manual_entries.all().active_entries()

    @cached_property
    def fetch_category_navigation(self):
        return self.category_navigation.all()

    def get_first_category(self):
        # TODO backwards compatibility, remove new release
        return self.categories.first()

    def get_category_navigation(self):
        # TODO backwards compatibility, remove new release
        return self.fetch_category_navigation

    @cached_property
    def fetch_category_navigation(self):
        category_navigation = []
        # if manual entries are selected the category navigation
        # is created from all distinct categories in selected entries
        if self.fetch_manual_entries:
            for entry in self.fetch_manual_entries:
                for category in entry.fetch_categories:
                    if category not in category_navigation:
                        category_navigation.append(category)
        else:
            # override auto category nav
            if self.fetch_category_navigation:
                for category in self.fetch_category_navigation:
                    if self.get_render_queryset_for_display(category).exists():
                        category_navigation.append(category)
            # auto category nav
            else:
                if self.fetch_categories:
                    for category in self.fetch_categories:
                        if self.get_render_queryset_for_display(category).exists():
                            category_navigation.append(category)
                # auto category nav, if no categories are specified
                else:
                    from allink_core.core_apps.allink_categories.models import AllinkCategory
                    categories = self.get_render_queryset_for_display().filter(~Q(categories=None)).values_list('categories')
                    category_navigation = list(AllinkCategory.objects.filter(id__in=categories).distinct())
        return category_navigation

    def _apply_filtering_to_queryset_for_display(self, queryset):
        """
        applies individual query filters on given queryset.
        override in app instance (i.e. events) for custom filters
        see allink_core/apps/events/abstract_models.py for reference
        """
        return queryset

    def _apply_ordering_to_queryset_for_display(self, queryset):
        # latest
        if self.manual_ordering == AllinkBaseAppContentPlugin.LATEST:
            return queryset.latest()
        # earliest
        elif self.manual_ordering == AllinkBaseAppContentPlugin.EARLIEST:
            return queryset.earliest()
        # A-Z
        elif self.manual_ordering == AllinkBaseAppContentPlugin.TITLE_ASC:
            return queryset.title_asc()
        # Z-A
        elif self.manual_ordering == AllinkBaseAppContentPlugin.TITLE_DESC:
            return queryset.title_desc()
        # random
        elif self.manual_ordering == AllinkBaseAppContentPlugin.RANDOM:
            return queryset.random()
        # category
        elif self.manual_ordering == AllinkBaseAppContentPlugin.CATEGORY:
            return queryset.category()
        else:
            return queryset.distinct()

    def get_render_queryset_for_display(self, category=None, filters={}, request=None):
        """
         returns all data_model objects distinct to id which are in the selected categories
          - category: category instance
          - filters: dict model fields and value
            -> adds additional query
        """

        # apply filters from request
        queryset = self._apply_filtering_to_queryset_for_display(self.data_model.objects.active().filter(**filters))

        if self.categories.exists() or category:
            if category:
                queryset = queryset.filter_by_category(category)
            else:
                queryset = queryset.filter_by_categories(categories=self.fetch_categories)

            if self.fetch_categories_and:
                queryset = queryset.filter_by_categories(categories=self.fetch_categories_and)

        ordered_qs = self._apply_ordering_to_queryset_for_display(queryset)

        # hook for prefetching related
        ordered_qs = self._get_queryset_with_prefetch_related(ordered_qs)

        return ordered_qs

    def _get_queryset_with_prefetch_related(self, ordered_qs):
        return ordered_qs.prefetch_related('translations', 'preview_image')


class AllinkBaseSearchPlugin(CMSPlugin):

    data_model = None

    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50,
        default='search_grid_static'
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

    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def get_model_name(self):
        return self.data_model._meta.model_name

    @cached_property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return ' '.join(css_classes)

    @classmethod
    def get_templates(cls):
        templates = ()
        for x, y in get_additional_templates('{}_search'.format(cls.data_model._meta.model_name)):
            templates += ((x, y),)
        return templates


class AllinkBaseFormPlugin(CMSPlugin):

    form_class = None

    send_internal_mail = models.BooleanField(
        _(u'Send internal e-mail'),
        default=True,
        help_text=_(u'Send confirmation mail to defined internal e-mail addresses.')
    )
    internal_email_addresses = ArrayField(
        models.EmailField(
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
        verbose_name=_(u'Internal e-mail addresses'),
    )
    from_email_address = models.EmailField(
        _(u'Sender e-mail address'),
        blank=True,
        null=True
    )
    send_external_mail = models.BooleanField(
        _(u'Send external e-mail'),
        default=True,
        help_text=_(u'Send confirmation mail to customer.')
    )
    thank_you_text = models.TextField(
        _(u'Thank you text'),
        blank=True,
        null=True,
        help_text=_(u'This text will be shown, after form completion.')
    )
    label_layout = models.CharField(
        _(u'Display labels'),
        max_length=15,
        choices=(
            ('stacked', 'Stacked with fields'),
            ('side_by_side', 'Side by side with fields'),
            ('placeholder', 'As placeholders'),
        ),
        default='stacked',
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

    def __str__(self):
        return 'Form Plugin'

    class Meta:
        abstract = True

    def get_form(self):
        return self.form_class()

    @cached_property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        css_classes.append('side-by-side') if self.label_layout == 'side_by_side' else None
        css_classes.append('placeholder-enabled') if self.label_layout == 'placeholder' else None
        return ' '.join(css_classes)


class AllinkAddressFieldsModel(models.Model):

    street = models.CharField(
        _(u'Street'),
        max_length=255,
        blank=True,
        null=True
    )
    street_nr = models.CharField(
        _(u'Street Nr.'),
        max_length=50,
        blank=True,
        null=True
    )
    street_additional = models.CharField(
        _(u'Address Additional'),
        max_length=255,
        blank=True,
        null=True
    )
    zip_code = ZipCodeField(
        _(u'Zip Code'),
        blank=True,
        null=True
    )
    place = models.CharField(
        _(u'Place'),
        max_length=255,
        blank=True,
        null=True
    )
    country = models.CharField(
        _(u'Country'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class AllinkContactFieldsModel(models.Model):

    phone = PhoneNumberField(
        _(u'Phone'),
        help_text=_(u'We automatically handle phone number formatting, Please provide the number in the following format "+41 43 123 45 67".'),
        blank=True,
        null=True
    )
    mobile = PhoneNumberField(
        _(u'Mobile'),
        help_text=_(u'We automatically handle phone number formatting, Please provide the number in the following format "+41 43 123 45 67".'),
        blank=True,
        null=True
    )
    fax = PhoneNumberField(
        _(u'Fax'),
        help_text=_(u'We automatically handle phone number formatting, Please provide the number in the following format "+41 43 123 45 67".'),
        blank=True,
        null=True
    )
    email = models.EmailField(
        _(u'Email'),
        blank=True,
        default=''
    )
    website = models.URLField(
        _(u'Website'),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    @cached_property
    def phone_formatted(self):
        if self.phone:
            x = phonenumbers.parse(str(self.phone), None)
            return (str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)))

    @cached_property
    def mobile_formatted(self):
        if self.mobile:
            x = phonenumbers.parse(str(self.mobile), None)
            return (str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)))

    @cached_property
    def fax_formatted(self):
        if self.fax:
            x = phonenumbers.parse(str(self.fax), None)
            return (str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)))

    @cached_property
    def website_clean(self):
        if self.website:
            website = urlparse(self.website)
            domain = '{uri.netloc}'.format(uri=website)
            return domain.replace('www.', '')


class AllinkInternalLinkFieldsModel(models.Model):
    #  Page redirect
    link_page = PageField(
        verbose_name=_(u'New Page'),
        null=True,
        on_delete=models.SET_NULL,
        help_text=_(u'If provided, overrides the external link and New Apphook-Page.'),
    )
    #  Fields for app redirect
    link_apphook_page = PageField(
        verbose_name=_(u'New Apphook-Page'),
        null=True,
        on_delete=models.SET_NULL,
        help_text=_(u'If provided, overrides the external link.'),
        related_name='%(app_label)s_%(class)s_app_legacy_redirects'
    )
    link_object_id = models.IntegerField(
        null=True,
        help_text=_(u'To which object directs the url.')
    )
    link_model = models.CharField(
        null=True,
        max_length=300,
        help_text=_(u'Dotted Path to referenced Model')
    )
    link_url_name = models.CharField(
        null=True,
        max_length=64,
        help_text=_(u'Name of the App-URL to use.')
    )
    link_url_kwargs = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True
        ),
        blank=True,
        null=True,
        help_text=_(u'Keyword arguments used to reverse url.')
    )

    class Meta:
        abstract = True

    @cached_property
    def link(self):
        if self.link_page:
            link = self.link_page.get_absolute_url()
        elif self.link_apphook_page:
            try:
                obj_model = get_model(self.link_model.split('.')[-3], self.link_model.split('.')[-1])
                obj = obj_model.objects.get(id=self.link_object_id)
                url_kwargs = {key: getattr(obj, key) for key in self.link_url_kwargs}
                url_name = u'{}:{}'.format(self.link_apphook_page.application_namespace, self.link_url_name)
                link = reverse(url_name, kwargs=url_kwargs)
            except:
                link = ''
        else:
            link = ''
        return link

    @cached_property
    def link_object(self):
        if self.link_page:
            link_obj = self.link_page
        elif self.link_apphook_page:
            try:
                obj_module = import_module('.'.join(self.link_model.split('.')[:-1]))
                obj_model = getattr(obj_module, self.link_model.split('.')[-1])
                link_obj = obj_model.objects.get(id=self.link_object_id)
            except:
                link_obj = None
        else:
            link_obj = None
        return link_obj

    @cached_property
    def is_page_link(self):
        if self.link_page:
            return True
        else:
            return False


class AllinkLinkFieldsModel(AllinkInternalLinkFieldsModel):
    link_url = models.URLField(
        verbose_name=(u'External link'),
        blank=True,
        default='',
        help_text=_(u'Provide a valid URL to an external website.'),
        max_length=500,
    )
    link_mailto = models.EmailField(
        verbose_name=_(u'Email address'),
        blank=True,
        null=True,
        max_length=255,
    )
    link_phone = models.CharField(
        verbose_name=_(u'Phone'),
        blank=True,
        null=True,
        max_length=255,
    )
    link_anchor = models.CharField(
        verbose_name=_(u'Anchor'),
        max_length=255,
        blank=True,
        help_text=_(u'Appends the value only after the internal or external link.<br>'
                    u'Do <strong>not</strong> include a preceding "#" symbol.'),
    )
    link_target = models.IntegerField(
        _(u'Link Target'),
        choices=TARGET_CHOICES,
        null=True,
        blank=True
    )
    link_file = FilerFileField(
        verbose_name=_(u'file'),
        null=True,
        blank=True
    )
    link_special = models.CharField(
        verbose_name=_(u'Special Links'),
        max_length=255,
        blank=True,
        null=True
    )
    link_attributes = AttributesField(
        verbose_name=_(u'Attributes'),
        blank=True,
        excluded_keys=['class', 'href', 'target'],
    )

    class Meta:
        abstract = True

    @cached_property
    def new_window_enabled(self):
        return True if self.link_target == NEW_WINDOW and not self.form_modal_enabled and not self.softpage_large_enabled and not self.softpage_small_enabled else False

    @cached_property
    def softpage_large_enabled(self):
        return True if self.link_target == SOFTPAGE_LARGE else False

    @cached_property
    def softpage_small_enabled(self):
        return True if self.link_target == SOFTPAGE_SMALL else False

    @cached_property
    def form_modal_enabled(self):
        return True if self.link_target == FORM_MODAL else False

    @cached_property
    def image_modal_enabled(self):
        return True if self.link_target == IMAGE_MODAL else False

    @property
    def default_modal_enabled(self):
        return True if self.link_target == DEFAULT_MODAL else False

    @classmethod
    def get_link_special_choices(self):
        return BLANK_CHOICE + get_additional_choices('BUTTON_LINK_SPECIAL_LINKS_CHOICES')

    def get_link_url(self):
        # TODO backwards compatibility, remove new release
        return self.link_url_typed

    @cached_property
    def link_url_typed(self):
        internal_link = self.link
        if internal_link:
            link = internal_link
        elif self.link_url:
            link = self.link_url
        elif self.link_phone:
            link = 'tel:{}'.format(self.link_phone.replace(' ', ''))
        elif self.link_mailto:
            link = 'mailto:{}'.format(self.link_mailto)
        elif self.link_file:
            link = self.link_file.url
        elif self.link_special:
            try:
                """
                because we are always in a plugin (e.g Button, Image..)
                and plugins can appear more than once on the same page,
                the urls should always pass a plugin_id (not all urls do at the moment)
                """
                link = reverse(self.link_special, kwargs={'plugin_id': self.id})
            except:
                link = reverse(self.link_special)
        else:
            link = ''
        if self.link_anchor:
            link += '#{}'.format(self.link_anchor)
        return link

    def clean(self):
        super(AllinkLinkFieldsModel, self).clean()
        field_names = (
            'link_url',
            'link_page',
            'link_apphook_page',
            'link_mailto',
            'link_phone',
            'link_file',
        )
        anchor_field_name = 'link_anchor'
        field_names_allowed_with_anchor = (
            'link_url',
            'link_page',
            'link_apphook_page',
            'link_file',
        )

        anchor_field_verbose_name = force_text(self._meta.get_field_by_name(anchor_field_name)[0].verbose_name)
        anchor_field_value = getattr(self, anchor_field_name)

        link_fields = {
            key: getattr(self, key)
            for key in field_names
        }
        link_field_verbose_names = {
            key: force_text(self._meta.get_field_by_name(key)[0].verbose_name)
            for key in link_fields.keys()
        }
        provided_link_fields = {
            key: value
            for key, value in link_fields.items()
            if value
        }

        if anchor_field_value:
            for field_name in provided_link_fields.keys():
                if field_name not in field_names_allowed_with_anchor:
                    error_msg = _('%(anchor_field_verbose_name)s is not allowed together with %(field_name)s') % {
                        'anchor_field_verbose_name': anchor_field_verbose_name,
                        'field_name': link_field_verbose_names.get(field_name)
                    }
                    raise ValidationError({
                        anchor_field_name: error_msg,
                        field_name: error_msg,
                    })


class AllinkSimpleRegistrationFieldsModel(TimeStampedModel):

    salutation = models.IntegerField(
        _(u'Salutation'),
        choices=SALUTATION_CHOICES,
        null=True
    )

    first_name = models.CharField(
        _(u'First Name'),
        max_length=255,
        null=True
    )

    last_name = models.CharField(
        _(u'Last Name'),
        max_length=255,
        null=True
    )

    email = models.EmailField(
        _(u'Email'),
        null=True
    )

    company_name = models.CharField(
        _(u'Company'),
        max_length=255,
        blank=True,
        null=True
    )
    phone = models.CharField(
        _(u'Phone'),
        max_length=30,
        blank=True,
        null=True
    )

    message = models.TextField(
        _(u'Message'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
