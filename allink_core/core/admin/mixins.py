from allink_core.core.admin.forms import AllinkCategoryAdminForm


__all__ = [
    'AllinkMediaAdminMixin',
    'AllinkSEOAdminMixin',
    'AllinkCategoryAdminMixin',
    'AllinkTeaserAdminMixin',
]


class AllinkMediaAdminMixin:
    """
    ModelAdmin mixin used to add custom css and js
    """

    class Media:
        from webpack_loader.utils import get_files
        js = (
            get_files('djangocms_custom_admin')[1]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[0]['publicPath'],

            )
        }


class AllinkSEOAdminMixin:
    """
    ModelAdmin mixin used in combination with AllinkSEOFieldsModel and AllinkSEOTranslatedFieldsModel
    """

    def get_seo_fieldsets(self):
        fieldsets = (
            ('SEO', {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'og_image',
                    'og_title',
                    'og_description',
                )
            }),
        )

        return fieldsets


class AllinkCategoryAdminMixin:
    """
    ModelAdmin mixin used in combination with AllinCategoryFieldsModel

    add:
    list_display = (... 'all_categories_column', ...)

    add:
    list_filter = (
        'status',
        ...
        ('categories', admin.RelatedOnlyFieldListFilter,),
    )
    """

    form = AllinkCategoryAdminForm

    def all_categories_column(self, object):
        return "\n|\n".join([c.name for c in object.categories.all()])

    all_categories_column.short_description = 'Categories'

    def get_category_fieldsets(self):
        fieldsets = ()
        if self.model.get_can_have_categories():
            fieldsets += (
                ('Categories', {
                    'fields': (
                        'categories',
                    )
                }),
            )
        return fieldsets


class AllinkTeaserAdminMixin:
    """
    ModelAdmin mixin used in combination with AllinkTeaserTranslatedFieldsModel
    """

    def get_teaser_fieldsets(self):
        fieldsets = (
            ('Teaser', {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'teaser_image',
                    'teaser_title',
                    'teaser_technical_title',
                    'teaser_description',
                    'teaser_link_text',
                    'teaser_link_url',
                )
            }),
        )

        return fieldsets
