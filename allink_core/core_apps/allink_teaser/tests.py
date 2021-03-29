from cms import api
from allink_core.core.test.base import PageApphookMixin
from django.test.testcases import TestCase
from allink_core.core.templatetags.allink_image_tags import get_width_alias_from_section_plugin
from allink_core.core_apps.allink_teaser.cms_plugins import CMSAllinkTeaserGridContainerPlugin, CMSAllinkTeaserPlugin


class ImageTagsSectionPluginUtilsTestCase(PageApphookMixin, TestCase):
    """
    As AllinkBaseSectionPlugin is an abstract model, we test the behavior regarding render_image
    on a CMSAllinkTeaserGridContainerPlugin.
    """
    colums = '1-of-3'
    position = 1  #

    def setUp(self):
        super().setUp()
        # CMSAllinkTeaserGridContainerPlugin, column='1-of-3'
        self.content_plugin = api.add_plugin(
            self.placeholder,
            CMSAllinkTeaserGridContainerPlugin,
            self.language,
            columns=self.colums
        )

        api.add_plugin(
            self.placeholder,
            CMSAllinkTeaserPlugin,
            self.language,
            target=self.content_plugin
        )

        self.teaser_plugin = self.content_plugin.get_children()[self.position - 1]

    def test_get_width_alias_from_section_plugin(self):
        result = get_width_alias_from_section_plugin(self.teaser_plugin)
        self.assertEqual('1-of-3', result)
