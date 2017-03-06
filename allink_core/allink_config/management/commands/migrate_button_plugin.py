from aldryn_bootstrap3.models import Boostrap3ButtonPlugin
from allink_core.djangocms_button_link.models import AllinkButtonLinkPlugin
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Migrate Boostrap3ButtonPlugin To AllinkButtonLinkPlugin'

    def handle(self, *args, **options):
        for old in Boostrap3ButtonPlugin.objects.all():
            new = AllinkButtonLinkPlugin()

            new.position = old.position
            new.language = old.language
            new.plugin_type = 'CMSAllinkButtonLinkPlugin'
            new.creation_date = old.creation_date
            new.changed_date = old.changed_date
            new.parent_id = old.parent_id
            new.placeholder_id = old.placeholder_id
            new.depth = old.depth
            new.numchild = old.numchild
            new.path = old.path

            new.link_url = old.link_url
            new.link_anchor = old.link_anchor
            new.link_mailto = old.link_mailto
            new.link_phone = old.link_phone
            new.link_target = old.link_target
            new.cmsplugin_ptr_id = old.cmsplugin_ptr_id
            new.label = old.label
            new.type = old.type
            new.btn_context = old.btn_context
            new.btn_size = old.btn_size
            new.btn_block = old.btn_block
            new.txt_context = old.txt_context
            new.icon_left = old.icon_left
            new.icon_right = old.icon_right
            new.extra_css_classes = old.classes
            new.link_file_id = old.link_file_id
            new.link_page_id = old.link_page_id
            new.link_attributes = old.link_attributes

            new.save()
