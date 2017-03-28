# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from cms.models.pluginmodel import CMSPlugin
from adminsortable.models import SortableMixin
from filer.fields.image import FilerImageField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from allink_core.allink_base.utils import get_additional_templates
from allink_core.allink_categories.models import AllinkCategory

from .choices import BLANK_CHOICE, TITLE_CHOICES, H1
from .model_fields import Classes
from .managers import AllinkBaseModelManager
from .reusable_fields import AllinkMetaTagFieldsModel


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

    """

    """
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

    created = AutoCreatedField(_('created'), editable=True)
    modified = AutoLastModifiedField(_('modified'))

    categories = models.ManyToManyField(
        AllinkCategory,
        blank=True
    )
    active = models.BooleanField(
        _(u'Active'),
        default=True
    )

    objects = AllinkBaseModelManager()

    class Meta:
        abstract = True
        app_label = 'allinkbasemodel'

    def __str__(self):
        return u'%s - %s' % (self.title, self.created.strftime('%d.%m.%Y'))

    @classmethod
    def get_published(cls):
        return cls.objects.filter(active=True)

    @classmethod
    def get_next(cls, instance):
        return cls.get_published().filter(created__gte=instance.created, id__gt=instance.id).exclude(id=instance.id).order_by('created', 'id').first()

    @classmethod
    def get_previous(cls, instance):
        return cls.get_published().filter(created__lte=instance.created, id__lt=instance.id).order_by('created', 'id').last()

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

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        app = '{}:detail'.format(self._meta.model_name)
        return reverse(app, kwargs={'slug': self.slug})


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
        choices=settings.PROJECT_COLORS,
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

    @classmethod
    def get_project_color_choices(cls):
        return BLANK_CHOICE + settings.PROJECT_COLORS

    @property
    def base_classes(self):
        css_classes = []
        css_classes.append("container-enabled") if self.container_enabled else None
        css_classes.append('section-heading-{}'.format(self.title_size)) if self.title_size else None
        css_classes.append("has-bg-color") if self.bg_color else None
        css_classes.append("has-bg-image") if self.bg_image_outer_container else None
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
        ('categories', _(u'Categories')),
    )

    # FIELDS
    categories = models.ManyToManyField(AllinkCategory, blank=True)
    # categories_and = models.ManyToManyField(AllinkCategory, blank=True)

    manual_ordering = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    filter_fields = ArrayField(models.CharField(
        max_length=50,
        choices=FILTER_FIELD_CHOICES,),
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
        default=9,
        help_text=_(u'Set to 0 if all entries should be displayed on first page.')
    )
    pagination_type = models.CharField(
        _(u'Paggination Type'),
        max_length=50,
        choices=PAGINATION_TYPE,
        default=PAGINATION_TYPE[0]
    )
    load_more_button_text = models.CharField(
        _(u'Text for "Load More"-Button'),
        help_text=_(u'If left blank, a default text will be used.'),
        max_length=255,
        null=True,
        blank=True
    )
    detail_link_text = models.CharField(
        _(u'Text for "Detail"-Link'),
        help_text=_(u'If left blank, a default text will be used.'),
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
        self.category_navigation = oldinstance.category_navigation.all()

    def get_model_name(self):
        return self.data_model._meta.model_name

    def get_fk_model(self, fieldname):
        """
        returns None if not foreignkey, otherswise the relevant model
        """
        from django.db.models import ForeignKey
        field_object, model, direct, m2m = self.data_model._meta.get_field_by_name(fieldname)
        if (direct and isinstance(field_object, ForeignKey)) or (direct and m2m):
            return field_object.rel.to
        return None

    def get_distinct_values_of_field(self, fieldname):
        """
        returns distinct values_list for fieldname
        """
        return self.get_render_queryset_for_display().order_by().values_list(fieldname).distinct()

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
            if self.get_fk_model(fieldname):
                filters.extend((entry.id, entry.__unicode__(),) for entry in
                               self.get_fk_model(fieldname).objects.filter(
                                   id__in=self.get_distinct_values_of_field(fieldname)))
                try:
                    # for apps with verbose names changed in allink_config
                    verbose_name = self.get_fk_model(fieldname).get_verbose_name()
                except:
                    verbose_name = self.get_fk_model(fieldname)._meta.verbose_name_plural
                options.update({verbose_name: filters})
            # field is no foreignkey and no m2m
            else:
                filters.extend((value[0], value[0],) for value in self.get_distinct_values_of_field(fieldname))
                options.update({fieldname: filters})
        return options

    def get_first_category(self):
        return self.categories.first()

    def get_category_navigation(self):
        category_navigation = []
        # override auto category nav
        if self.category_navigation:
            for category in self.category_navigation:
                if self.get_render_queryset_for_display(category).exists():
                    category_navigation.append(category)
        # auto category nav
        else:
            for category in self.categories.all():
                if self.get_render_queryset_for_display(category).exists():
                    category_navigation.append(category)
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
            return queryset

    def get_render_queryset_for_display(self, category=None, filter=None):
        """
         returns all data_model objects distinct to id which are in the selected categories
          - category: category instance
          - filter: list tuple with model fields and value
            -> adds additional query

        -> Is also defined in  AllinkManualEntriesMixin to handel manual entries !!
        """
        if self.categories.count() > 0 or category:
            """
             category selection
            """
            if category:
                queryset = self.data_model.objects.filter_by_category(category)
            else:
                queryset = self.data_model.objects.filter_by_categories(self.categories)

            return self._apply_ordering_to_queryset_for_display(queryset)

        else:
            queryset = self.data_model.objects.active()
            return queryset
