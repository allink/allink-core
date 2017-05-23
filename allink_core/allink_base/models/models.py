# -*- coding: utf-8 -*-
import urllib.parse
from django.conf import settings
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.core.urlresolvers import NoReverseMatch
from django.core.exceptions import FieldDoesNotExist, FieldError, ValidationError
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, override
from cms.utils.i18n import get_current_language, get_default_language
from cms.models.pluginmodel import CMSPlugin

from adminsortable.models import SortableMixin
from filer.fields.image import FilerImageField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from allink_core.allink_base.utils import base_url, get_additional_templates
from allink_core.allink_categories.models import AllinkCategory

from allink_core.allink_base.models import Classes
from allink_core.allink_base.models import AllinkBaseModelManager
from allink_core.allink_base.models import AllinkMetaTagFieldsModel
from allink_core.allink_base.models.choices import TITLE_CHOICES, H1


@python_2_unicode_compatible
class AllinkBaseImage(SortableMixin):
    """
    Abstract Image class for BaseApps with image Gallery

    """
    # title = models.CharField(max_length=255, validators=[MaxLengthValidator(255)], blank=True, null=True)
    image = FilerImageField(
        default=None,
        null=True
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('sort_order',)

    def __str__(self):
        return str(self.image.filer_image_file)


@python_2_unicode_compatible
class AllinkBaseModel(AllinkMetaTagFieldsModel):
    """
     An abstract base class model for every standard allink app

     translateable fields defined in child model because parler can't handle translation override in abstract models
          -> Translated Fields have to be specified in the child model

              title = models.CharField(max_length=255, validators=[MaxLengthValidator(255)])
              slug = models.SlugField(_(u'Slug'),
                                       max_length=255,
                                       default='',
                                       blank=True,
                                       help_text=_(u"Leave blank to auto-generate a unique slug."))

    -> the AllinkBaseAdmin class expects the fields: 'title' and 'slug'

    """

    # Is used to auto generate Category
    category_name_field = u'title'

    created = AutoCreatedField(_('created'), editable=True)
    modified = AutoLastModifiedField(_('modified'))

    categories = models.ManyToManyField(
        AllinkCategory,
        blank=True
    )
    is_active = models.BooleanField(
        _(u'Active'),
        default=True
    )
    auto_generated_category = models.OneToOneField(
        AllinkCategory,
        related_name=u'auto_generated_from_%(class)s',
        null=True,
        blank=True,
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
        return cls.get_published().filter(created__gte=instance.created, id__gt=instance.id).exclude(id=instance.id).order_by('created', 'id').first()

    @classmethod
    def get_previous(cls, instance):
        return cls.get_published().filter(created__lte=instance.created, id__lt=instance.id).order_by('created', 'id').last()

    @classmethod
    def get_relevant_categories(cls):
        """
        returns a queryset of all relevant categories for a the model_name
        """
        result = AllinkCategory.objects.none()
        for root in AllinkCategory.get_root_nodes().filter(model_names__contains=[cls._meta.model_name]):
            result |= root.get_descendants()
        return result

    @property
    def next(self):
        return self.get_next(self)

    @property
    def previous(self):
        return self.get_previous(self)

    @property
    def show_detail_link(self):
        if getattr(self, 'text'):
            return True
        else:
            return True if getattr(self, 'content_placeholder') else False

    @classmethod
    def get_can_have_categories(cls):
        if cls._meta.model_name in dict(settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES):
            return True
        else:
            return False

    @classmethod
    def get_verbose_name(cls):
        try:
            from allink_core.allink_config.models import AllinkConfig
            field_name = cls._meta.model_name + '_verbose'
            return getattr(AllinkConfig.get_solo(), field_name)
        except:
            return cls._meta.verbose_name

    @classmethod
    def get_verbose_name_plural(cls):
        try:
            from allink_core.allink_config.models import AllinkConfig
            field_name = cls._meta.model_name + '_verbose_plural'
            return getattr(AllinkConfig.get_solo(), field_name)
        except:
            return cls._meta.verbose_name_plural

    def is_published(self):
        return self in self.get_published()

    is_published.short_description = _(u'Published')
    is_published.boolean = True

    def get_detail_view(self):
        return '{}:detail'.format(self._meta.model_name)

    def get_absolute_url(self, language=None):
        from django.core.urlresolvers import reverse
        if not language:
            language = get_current_language() or get_default_language()

        slug, language = self.known_translation_getter(
            'slug', None, language_code=language)
        app = self.get_detail_view()
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
class AllinkBasePlugin(CMSPlugin):
    title = models.CharField(
        _(u'Title'),
        help_text=_(u'The section title'),
        max_length=255,
        blank=True,
        null=True
    )
    title_size = models.CharField(
        _(u'Section Title Size'),
        max_length=50,
        choices=TITLE_CHOICES,
        default=H1
    )
    container_enabled = models.BooleanField(
        _(u'Activate "container"'),
        help_text=_(u'If checked, an inner container with a maximum width is added'),
        default=True
    )
    bg_color = models.CharField(
        _(u'Set a predefined background color'),
        max_length=50,
        blank=True,
        null=True
    )
    bg_image_outer_container = FilerImageField(
        verbose_name=_(u'Background-Image'),
        help_text=_(u'Optional: Set a background image for the content section.<br>Note: This is meant for decorative purposes only and should be used with care.'),
        related_name='%(app_label)s_%(class)s_bg_image',
        blank=True,
        null=True
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
    extra_css_classes = Classes()

    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
    )

    class Meta:
        abstract = True

    @property
    def base_classes(self):
        css_classes = []
        css_classes.append("container-enabled") if self.container_enabled else None
        css_classes.append('section-heading-{}'.format(self.title_size)) if self.title_size else None
        css_classes.append("has-bg-color") if self.bg_color else None
        css_classes.append(self.bg_color) if self.bg_color else None
        if getattr(self, 'project_css_classes'):
            for css_class in getattr(self, 'project_css_classes'):
                css_classes.append(css_class)
        return css_classes

    def get_app_can_have_categories(self):
        if self.data_model._meta.model_name in dict(settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES):
            return True
        else:
            return False

    def __str__(self):
        if self.title:
            return u'{}'.format(self.title)
        return str(self.pk)


@python_2_unicode_compatible
class AllinkBaseAppContentPlugin(AllinkBasePlugin):
    """
    Base plugin which provides standard functionality to inherit from
    all Apps should inherit from this, to create a "app pointer plugin"

    - allows to display application content for different apps
    - ability to filter and sort entries
    - manually select entries (search entries and select/ sort)

    display opitions:
    - amount of entries on first page
    - coulmn amount
    - how to display detail page (softpage or external page)
    - paggination ("Load more", "1 2 3 ... 4 5")


    Future Features:
    - ?

    """

    data_model = None

    # TEMPLATES
    GRID_DYNAMIC = 'grid_dynamic'
    GRID_STATIC = 'grid_static'
    LIST = 'list'
    SLIDER = 'slider'
    TABLE = 'table'

    TEMPLATES = (
        (GRID_STATIC, 'Grid (Static)'),
        (GRID_DYNAMIC, 'Grid (Dynamic)'),
        (LIST, 'List'),
        (SLIDER, 'Slider'),
        (TABLE, 'Table'),
    )

    # PAGGINATION
    NO = 'no'
    LOAD = 'load'
    # PAGES = 'pages'

    PAGINATION_TYPE = (
        (NO, 'None'),
        (LOAD, 'Add "Load More"-Button'),
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

    ORDERING = (
        (DEFAULT, '---------'),
        (TITLE_ASC, 'A-Z (title)'),
        (TITLE_DESC, 'Z-A (title'),
        (LATEST, 'latest first'),
        (EARLIEST, 'earliest first'),
        (RANDOM, 'random'),
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

    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50,
        default=TEMPLATES[0]
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
        _(u'Paggination Type'),
        max_length=50,
        choices=PAGINATION_TYPE,
        default=PAGINATION_TYPE[0]
    )
    load_more_button_text = models.CharField(
        _(u'Text for "Load More"-Button'),
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

    class Meta:
        abstract = True

    def __str__(self):
        if self.title:
            return u'{}'.format(self.title)
        return str(self.pk)

    @classmethod
    def get_templates(cls):
        templates = cls.TEMPLATES
        for x, y in get_additional_templates(cls.data_model._meta.model_name):
            templates += ((x, y),)
        return templates

    @classmethod
    def get_ordering_choices(cls):
        return cls.ORDERING

    @property
    def css_classes(self):
        css_classes = self.base_classes
        css_classes.append('{}-template'.format(self.template)) if self.template else None
        css_classes.append('items-per-row-{}'.format(self.items_per_row)) if self.items_per_row else None
        return ' '.join(css_classes)

    def copy_relations(self, oldinstance):
        self.categories = oldinstance.categories.all()
        self.categories_and = oldinstance.categories_and.all()
        self.category_navigation = oldinstance.category_navigation.all()

    def get_model_name(self):
        return self.data_model._meta.model_name

    def get_correct_template(self, file='content'):

        template = '{}/plugins/{}/{}.html'.format(self.data_model._meta.app_label, self.template, file)

        # check if project specific template
        try:
            get_template(template)
        except TemplateDoesNotExist:
            try:
                template = 'app_content/plugins/{}/{}.html'.format(self.template, file)
                get_template(template)
            except TemplateDoesNotExist:
                # we can't guess all possible custom templates
                # so this is a fallback for all custom plugins
                template = 'app_content/plugins/{}/{}.html'.format('grid_static', file)
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
            return self.get_render_queryset_for_display().filter(**query_filter).order_by().values_list(fieldname).distinct()
        # handle translated fields
        except FieldError:
            translation_model = self.data_model.translations.related.related_model
            model_query = self.get_render_queryset_for_display().filter(**query_filter)
            return translation_model.objects.filter(language_code=get_current_language(), master__in=model_query).order_by().values_list(fieldname).distinct()

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

    def get_first_category(self):
        return self.categories.first()

    def get_category_navigation(self):
        category_navigation = []
        # override auto category nav
        if self.category_navigation.exists():
            for category in self.category_navigation.all():
                if self.get_render_queryset_for_display(category).exists():
                    category_navigation.append(category)
        # auto category nav
        else:
            if self.categories.exists():
                for category in self.categories:
                    if self.get_render_queryset_for_display(category).exists():
                        category_navigation.append(category)
            # auto category nav, if no categories are specified
            else:
                from allink_core.allink_categories.models import AllinkCategory
                categories = self.get_render_queryset_for_display().filter(~Q(categories=None)).values_list('categories')
                category_navigation = list(AllinkCategory.objects.filter(id__in=categories).distinct())
        return category_navigation

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
        else:
            return queryset.distinct()

    def get_render_queryset_for_display(self, category=None, filters={}):
        """
         returns all data_model objects distinct to id which are in the selected categories
          - category: category instance
          - filters: dict model fields and value
            -> adds additional query
        """

        # apply filters from request
        queryset = self.data_model.objects.active().filter(**filters)

        if self.categories.exists() or category:
            if category:
                queryset = queryset.filter_by_category(category)
            else:
                queryset = queryset.filter_by_categories(categories=self.categories.all())

            if self.categories_and.exists():
                queryset = queryset.filter_by_categories(categories=self.categories_and.all())

        return self._apply_ordering_to_queryset_for_display(queryset)


class AllinkBaseFormPlugin(CMSPlugin):

    form_class = None

    send_internal_mail = models.BooleanField(
        _(u'Send internal e-mail'),
        default=True,
        help_text=_(u'Send confirmation mail to defined internal e-mail addresses.')
    )
    internal_email_adresses = ArrayField(
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
    )
    label_layout = models.CharField(
        _(u'Display labels'),
        max_length=15,
        choices=(
            ('side_by_side', 'Side by side with fields'),
            ('stacked', 'Stacked with fields'),
            ('placeholder', 'As placeholders'),
        ),
        default='stacked',
    )
    form_css_classes = ArrayField(
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

    @property
    def css_classes(self):
        css_classes = []
        if getattr(self, 'form_css_classes'):
            for css_class in getattr(self, 'form_css_classes'):
                css_classes.append(css_class)
        css_classes.append('side-by-side') if self.label_layout == 'side_by_side' else None
        css_classes.append('placeholder-enabled') if self.label_layout == 'placeholder' else None
        return ' '.join(css_classes)
