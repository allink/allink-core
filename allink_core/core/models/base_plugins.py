# -*- coding: utf-8 -*-
import urllib.parse
from django.conf import settings
from django.db import models
from django.db.models import Q, QuerySet
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from cms.utils.i18n import get_current_language
from cms.models.pluginmodel import CMSPlugin

from allink_core.core.utils import get_additional_templates
from allink_core.core.models.fields import CMSPluginField
from allink_core.core_apps.allink_categories.models import AllinkCategory

__all__ = [
    'AllinkBaseAppContentPlugin',
    'AllinkBaseFormPlugin',
    'AllinkBaseSearchPlugin',
]


class AllinkBaseAppContentPlugin(CMSPlugin):
    """
    TODO
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
        #     'verbose': _('Categories'),
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
        _('Template'),
        help_text=_('Choose a template.'),
        max_length=50
    )
    category_navigation_enabled = models.BooleanField(
        _('Show category navigation'),
        help_text=_(
            u'If checked, a filter navigation with all selected categories is displayed.'
            u'<br>Please note: A category is only displayed if it contains items.'),
        default=False
    )
    category_navigation_all = models.BooleanField(
        _('Show category "all"'),
        help_text=_('If checked, a category "all" in filter navigation is displayed.'),
        default=False
    )
    category_navigation = models.ManyToManyField(
        AllinkCategory,
        related_name='%(app_label)s_%(class)s_category_navigation',
        verbose_name=_('Categories for Navigation'),
        help_text=_(
            u'You can explicitly define the categories for the category navigation here.'
            u' This will override the automatically set of categories'
            u' (either the one generated from "Filter & Ordering" or "Manual entries")'),
        blank=True,
    )
    softpage_enabled = models.BooleanField(
        _('Show detailed information in Softpage'),
        help_text=_(
            u'If checked, the detail view of an entry will be displayed in a "softpage".'
            u' Otherwise the page will be reloaded.'),
        default=True
    )
    detail_link_enabled = models.BooleanField(
        _('Show detail link'),
        help_text=_('If checked, a link/button to the detail view will be displayed.'),
        default=True
    )
    items_per_row = models.IntegerField(
        _('Grid items per row'),
        help_text=_('Only applied if a "Grid" template has been selected.'),
        choices=COLUMN_AMOUNT,
        default=3
    )
    paginated_by = models.IntegerField(
        _('Max. entries per page'),
        default=0,
        help_text=_(
            u'Limit the number of entries (in case of the "load more" pagination type: entries per page).'
            u' Default is "0" (show all entries)')
    )
    pagination_type = models.CharField(
        _('Pagination Type'),
        max_length=50,
        choices=PAGINATION_TYPE,
        default=PAGINATION_TYPE[0]
    )
    load_more_button_text = models.CharField(
        _('Text for "Load .."-Button'),
        help_text=_(
            u'If left blank, a default text will be used. <br>Note: Should the default text be adjusted site-wide,'
            u' please contact the project manager (such changes can be made on a code level)'),
        max_length=255,
        null=True,
        blank=True
    )
    detail_link_text = models.CharField(
        _('Text for "Detail"-Link'),
        help_text=_(
            u'If left blank, a default text will be used.<br>Note: Should the default text be adjusted site-wide,'
            u' please contact the project manager (such changes can be made on a code level)'),
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
    cmsplugin_ptr = CMSPluginField()

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
        for i in oldinstance.categories.all():
            self.categories.add(i)
        for i in oldinstance.categories_and.all():
            self.categories_and.add(i)
        for i in oldinstance.category_navigation.all():
            self.category_navigation.add(i)
        for i in oldinstance.manual_entries.all():
            self.manual_entries.add(i)

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
            field_object, model, direct, m2m = self.data_model._meta.get_field(fieldname)
        # in case that the field is translated, it can't be found on the model itself
        # so we get the translationmodel and get all data from there.
        except FieldDoesNotExist:
            is_translated = True
            field_object, model, direct, m2m = self.data_model.translations.related.related_model. \
                _meta.get_field(fieldname)
        if (direct and isinstance(field_object, ForeignKey)) or (direct and m2m):
            return field_object.rel.to, is_translated
        return None, is_translated

    def get_distinct_values_of_field(self, fieldname):
        """
        returns distinct values_list for fieldname
        the query_filter defined in FILTER_FIELD_CHOICES gets applied here
        """
        try:
            query_filter = {u'%s__%s' % (fieldname, k): v for k, v in
                            dict(self.FILTER_FIELD_CHOICES)[fieldname]['query_filter'].items()}
        except KeyError:
            query_filter = {}
        try:
            # order alphabetically if not 'categories' (they are ordered by 'lft')
            order_by = fieldname if fieldname != 'categories' else 'lft'
            return self.get_render_queryset_for_display().filter(**query_filter).order_by(order_by).values_list(
                fieldname).distinct()
        # handle translated fields
        except FieldError:
            translation_model = self.data_model.translations.related.related_model
            model_query = self.get_render_queryset_for_display().filter(**query_filter)
            return translation_model.objects.filter(language_code=get_current_language(),
                                                    master__in=model_query).order_by(order_by).values_list(
                fieldname).distinct()

    def get_filter_fields_with_options(self):
        """
        returns dict with all filter fields and there distinct values of the particular model field
        (e.g. list of {categories: [(10, 'News')..], place: [2, 'Zürich']}
        TODO: at the moment only one value for "filter_fields" is supported. (makes "load more" logic simpler)
        """
        options = {}
        for fieldname in self.filter_fields:
            # field is foreignkey or m2m, so we have to get the verbose name form the model itself
            filters = [((None, _('All'),))]
            fk_model, is_translated = self.get_field_info(fieldname)
            if fk_model:
                filters.extend((entry.id, entry.__str__(),) for entry in
                               fk_model.objects.filter(
                                   id__in=self.get_distinct_values_of_field(fieldname)))
            # field is no foreignkey and no m2m
            else:
                filters.extend((urllib.parse.quote_plus(value[0]), value[0]) for value in
                               self.get_distinct_values_of_field(fieldname))
            filter_key = "%s-translations__%s" % (
                self.data_model._meta.model_name, fieldname) if is_translated else "%s-%s" % (
                self.data_model._meta.model_name, fieldname)
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
        return self.manual_entries.all().active()

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
            if self.category_navigation.exists():
                for category in self.category_navigation.all():
                    if isinstance(self.get_render_queryset_for_display(category), QuerySet):
                        if self.get_render_queryset_for_display(category).exists():
                            category_navigation.append(category)
                    else:
                        if len(self.get_render_queryset_for_display(category)):
                            category_navigation.append(category)
            # auto category nav
            else:
                if self.fetch_categories:
                    for category in self.fetch_categories:
                        if len(self.get_render_queryset_for_display(category)) or self.get_render_queryset_for_display(
                           category).exists():
                            category_navigation.append(category)
                # auto category nav, if no categories are specified
                else:
                    from allink_core.core_apps.allink_categories.models import AllinkCategory
                    categories = self.get_render_queryset_for_display().filter(~Q(categories=None)).values_list(
                        'categories')
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
            # return queryset.category()
            # https://code.djangoproject.com/ticket/24218
            distinct_people = []
            for person in queryset.category():
                if person not in distinct_people:
                    distinct_people.append(person)
            return distinct_people
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
        if type(ordered_qs) is list:
            return ordered_qs
        return ordered_qs.prefetch_related('translations', 'preview_image')


class AllinkBaseSearchPlugin(CMSPlugin):
    data_model = None

    template = models.CharField(
        _('Template'),
        help_text=_('Choose a template.'),
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

    cmsplugin_ptr = CMSPluginField()

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
        for x, y in get_additional_templates('{}_SEARCH'.format(cls.data_model._meta.model_name)):
            templates += ((x, y),)
        return templates


class AllinkBaseFormPlugin(CMSPlugin):
    form_class = None

    send_internal_mail = models.BooleanField(
        _('Send internal e-mail'),
        default=True,
        help_text=_('Send confirmation mail to defined internal e-mail addresses.')
    )
    internal_email_addresses = ArrayField(
        models.EmailField(
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
        verbose_name=_('Internal e-mail addresses'),
    )
    from_email_address = models.EmailField(
        _('Sender e-mail address'),
        blank=True,
        null=True
    )
    send_external_mail = models.BooleanField(
        _('Send external e-mail'),
        default=True,
        help_text=_('Send confirmation mail to customer.')
    )
    thank_you_text = models.TextField(
        _('Thank you text'),
        blank=True,
        null=True,
        help_text=_('This text will be shown, after form completion.')
    )
    label_layout = models.CharField(
        _('Display labels'),
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
