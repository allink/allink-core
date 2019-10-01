from import_export import resources, fields

from allink_core.core_apps.allink_legacy_redirect.models import AllinkLegacyLink


class AllinkLegacyLinkResource(resources.ModelResource):
    old = fields.Field(column_name='target', attribute='old')

    class Meta:
        model = AllinkLegacyLink
        fields = ['old']
        import_id_fields = ['old']
        skip_unchanged = True

    def skip_row(self, instance, original):
        out = super(AllinkLegacyLinkResource, self).skip_row(instance, original)
        # skip urls which we never want to be redirected
        if not out and instance.old in ['(not set)','/']:
            return True
        return out
