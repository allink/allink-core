# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from model_utils.models import TimeStampedModel
from adminsortable.models import SortableMixin
from filer.fields.image import FilerImageField

from allink_core.allink_base.utils import get_additional_templates
from allink_core.allink_categories.models import AllinkCategory

from .choices import TITLE_CHOICES, H1
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
class AllinkBaseModel(AllinkMetaTagFieldsModel, TimeStampedModel):
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

    @classmethod
    def get_can_have_categories(cls):
        if cls._meta.model_name in dict(settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES):
            return True
        else:
            return False

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
    bg_color = models.IntegerField(
        _(u'Set a predefined background color'),
        choices=enumerate(settings.PROJECT_COLORS),
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
        css_classes.append(self.get_bg_color_display()) if self.bg_color else None
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
    - ? (should a "tab filtering" option be displayed? if so, which category)
    - ? (should a search field be displayed?)

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
    TITLE_ASC = 'title_asc'
    TITLE_DESC = 'title_desc'
    LATEST = 'latest'
    OLDEST = 'oldest'


    ORDERING = (
        (TITLE_ASC, 'A-Z (title)'),
        (TITLE_DESC, 'Z-A (title'),
        (LATEST, 'latest first'),
        (OLDEST, 'oldest first'),
    )

    # FIELDS
    categories = models.ManyToManyField(AllinkCategory, blank=True)

    manual_ordering = models.CharField(
        max_length=50,
        choices=ORDERING,
        null=True,
        blank=True
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
    softpage_enabled = models.BooleanField(
        _(u'Show detailed information in Softpage'),
        help_text=_(u'If checked, the detail view of an entry will be displayed in a "softpage". Otherwise the page will be reloaded)'),
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
    # bg_image_outer_container = FilerImageField(
    #     verbose_name=_(u'Background-Image'),
    #     help_text=_(u'Dimensions TBD'),
    #     related_name='app_content_bg_image',
    #     blank=True,
    #     null=True
    # )

    class Meta:
        abstract = True

    def __str__(self):
        if self.title:
            return u'{}'.format(self.title)
        return str(self.pk)

    @property
    def css_classes(self):
        css_classes = self.base_classes
        css_classes.append('{}-template'.format(self.template)) if self.template else None
        css_classes.append('items-per-row-{}'.format(self.items_per_row)) if self.items_per_row else None
        return ' '.join(css_classes)

    def copy_relations(self, oldinstance):
        self.categories = oldinstance.categories.all()

    def get_templates(self):
        for x, y in get_additional_templates(self.data_model._meta.model_name):
            self.TEMPLATES += ((x, y),)
        return self.TEMPLATES

    def get_first_category(self):
        return self.categories.first()

    def get_category_navigation(self):
        category_navigation = []
        for category in self.categories.all():
            if self.get_render_queryset_for_display(category).exists():
                category_navigation.append(category)
        return category_navigation

    def _apply_ordering_to_queryset_for_display(self, queryset):
        # latest
        if self.manual_ordering == AllinkBaseAppContentPlugin.LATEST:
            return queryset.latest()
        # oldest
        elif self.manual_ordering == AllinkBaseAppContentPlugin.OLDEST:
            return queryset.oldest()
        # A-Z
        elif self.manual_ordering == AllinkBaseAppContentPlugin.TITLE_ASC:
            return queryset.title_asc()
        # Z-A
        elif self.manual_ordering == AllinkBaseAppContentPlugin.TITLE_DESC:
            return queryset.title_desc()
        else:
            return queryset

    def get_render_queryset_for_display(self, category=None):
        """
        returns all data_model objects distinct to id which are in the selected categories
        """
        cat = None
        # performance enhancement when only one category
        if category or self.categories.count == 1:
            cat = category.id

        if self.categories.count() > 0:
            if cat:
                queryset = self.data_model.objects.filter_by_category(cat)
            else:
                queryset = self.data_model.objects.filter_by_categories(self.categories)
        else:
            if cat:
                queryset = self.manual_entries.select_related().order_by('id').filter_by_category(cat)
            else:
                queryset = self.manual_entries.select_related()

        return self._apply_ordering_to_queryset_for_display(queryset)
