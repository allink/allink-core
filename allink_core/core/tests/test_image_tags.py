from unittest import mock
from django.test.testcases import TestCase
from django.template import Context, Template
from cms import api
from easy_thumbnails.exceptions import InvalidImageFormatError
from allink_core.core.test.base import PageApphookMixin, GenericPluginMixin
from allink_core.core.utils import get_ratio_w_h, get_height_from_ratio
from allink_core.core.test.factories import FilerImageFactory
from allink_core.core.templatetags.allink_image_tags import (
    get_sizes_from_width_alias, get_width_alias_from_plugin, render_image,
)
from allink_core.core_apps.allink_content.cms_plugins import CMSAllinkContentPlugin, CMSAllinkContentColumnPlugin
from allink_core.core_apps.allink_image.cms_plugins import CMSAllinkImagePlugin


class MockThumbnailer(mock.Mock):
    def get_thumbnail(*args, **kwargs):
        return None


THUMBNAIL_WIDTH_ALIASES = {
    '1-of-1': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 1200, 'ratio': '3-2'},
        'xl': {'width': 1500, 'ratio': '3-2'}
    },
    '1-of-2': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 650, 'ratio': '3-2'},
        'xl': {'width': 900, 'ratio': '3-2'}
    },
    '2-of-3': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 600, 'ratio': '3-2'},
        'xl': {'width': 800, 'ratio': '3-2'}
    },
    '1-of-3': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 400, 'ratio': '3-2'},
        'xl': {'width': 400, 'ratio': '3-2'}
    },
    '1-of-4': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 500, 'ratio': '3-2'},
        'xl': {'width': 500, 'ratio': '3-2'}
    },
    'test-original': {
        'xs': {'width': 450, 'ratio': 'x-y'},
        'sm': {'width': 500, 'ratio': 'x-y'},
        'xl': {'width': 500, 'ratio': 'x-y'}
    },
}


class ImageTagsUtilsTestCase(TestCase):

    def test_get_ratio_w_h(self):
        ratio = '3-2'
        expected_w_h = (3, 2)
        result = get_ratio_w_h(ratio)
        self.assertEqual(expected_w_h, result)

    def test_get_height_from_ratio(self):
        width = 450
        ratio_w = 3
        ratio_h = 2

        expected_h = width * ratio_h / ratio_w  # 300

        result = get_height_from_ratio(width, ratio_w, ratio_h)
        self.assertEqual(expected_h, result)

    def test_get_sizes_from_width_alias(self):
        alias = '1-of-1'
        expected_sizes = [
            ('xs', (450, 300)),
            ('sm', (1200, 800)),
            ('xl', (1500, 1000)),
        ]
        result = get_sizes_from_width_alias(alias, image=None)
        self.assertListEqual(expected_sizes, result)

    def test_get_sizes_from_width_alias_original(self):
        alias = 'test-original'
        expected_sizes = [
            ('xs', (450, 225)),
            ('sm', (500, 250)),
            ('xl', (500, 250)),
        ]

        image = mock.MagicMock()
        image.width = 1000
        image.height = 500

        result = get_sizes_from_width_alias(alias, image=image)
        self.assertListEqual(expected_sizes, result)


class ImageTagsImagePluginUtilsTestCase(GenericPluginMixin, TestCase):
    plugin_class = CMSAllinkImagePlugin

    def test_get_width_alias_from_plugin_no_context_3(self):
        result = get_width_alias_from_plugin(self.plugin_model_instance)
        self.assertEqual('2-of-3', result)


class ImageTagsContentPluginUtilsTestCase(PageApphookMixin, TestCase):
    template = 'col-1'
    position = 1  #

    def setUp(self):
        super().setUp()
        # AllinkContentPlugin, template='col-1'
        self.content_plugin = api.add_plugin(
            self.placeholder,
            CMSAllinkContentPlugin,
            self.language,
            template=self.template
        )
        # AllinkContentColumnPlugin, template='col-1'
        column_amount = CMSAllinkContentPlugin.model.get_template_column_count(self.content_plugin.template)

        for x in range(int(column_amount)):
            api.add_plugin(
                self.placeholder,
                CMSAllinkContentColumnPlugin,
                self.language,
                target=self.content_plugin
            )

        self.column_plugin = self.content_plugin.get_children()[self.position - 1]

        # AllinkImagePlugin, inside column plugin
        self.image_plugin = api.add_plugin(
            self.placeholder,
            CMSAllinkImagePlugin,
            self.language,
            target=self.column_plugin
        )

    def test_get_width_alias_from_plugin_no_context_1(self):
        """ template col-1 """

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('1-of-1', result)

    def test_get_width_alias_from_plugin_no_context_1_1(self):
        self.content_plugin.template = 'col-1-1'
        self.content_plugin.save()

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('1-of-2', result)

    def test_get_width_alias_from_plugin_no_context_1_2_pos_0(self):
        self.content_plugin.template = 'col-1-2'
        self.content_plugin.save()

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('1-of-3', result)

    def test_get_width_alias_from_plugin_no_context_1_2_pos_1(self):
        self.content_plugin.template = 'col-1-2'
        self.content_plugin.save()
        self.column_plugin.position = 1
        self.column_plugin.save()

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('2-of-3', result)

    def test_get_width_alias_from_plugin_no_context_2_1_pos_0(self):
        self.content_plugin.template = 'col-2-1'
        self.content_plugin.save()

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('2-of-3', result)

    def test_get_width_alias_from_plugin_no_context_2_1_pos_1(self):
        self.content_plugin.template = 'col-2-1'
        self.content_plugin.save()
        self.column_plugin.position = 1
        self.column_plugin.save()

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('1-of-3', result)

    def test_get_width_alias_from_plugin_no_context_3(self):
        self.content_plugin.template = 'col-3'
        self.content_plugin.save()

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('1-of-3', result)

    def test_get_width_alias_from_plugin_no_context_4(self):
        self.content_plugin.template = 'col-4'
        self.content_plugin.save()

        result = get_width_alias_from_plugin(self.image_plugin)
        self.assertEqual('1-of-4', result)


class ImageTagsImagePluginContextTestCase(TestCase):
    """
    used width_alias:

    '1-of-4': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 500, 'ratio': '3-2'},
        'xl': {'width': 500, 'ratio': '3-2'}
    },

    expected context:
    {
        'instance': {'id': 1},

        'image', Image:

        'icon_enabled': True,
        'bg_enabled': True,
        'bg_color': None,
        'lazyload_enabled': True,
        'alt_text': '',
        'vh_enabled': False,

        'ratio_percent_xs': '66.66666666666666%',
        'ratio_vh_xs': '66.66666666666666vh',
        'thumbnail_xs', ThumbnailFile: filer_public_thumbnails/filer_public/a6/34/a634ad24-214f-400c-8957-90c3a23d3da0/so.png__450x300.0_q60_HIGH_RESOLUTION_crop-smart_subsampling-2_upscale.jpg>,

        'ratio_percent_sm': '66.66666666666666%',
        'ratio_vh_sm': '66.66666666666666vh',
        'thumbnail_sm', ThumbnailFile: filer_public_thumbnails/filer_public/a6/34/a634ad24-214f-400c-8957-90c3a23d3da0/so.png__600x400.0_q60_HIGH_RESOLUTION_crop-smart_subsampling-2_upscale.jpg>,

        'ratio_percent_xl': '66.66666666666667%',
        'ratio_vh_xl': '66.66666666666667vh',
        'thumbnail_xl', ThumbnailFile: filer_public_thumbnails/filer_public/a6/34/a634ad24-214f-400c-8957-90c3a23d3da0/so.png__800x533.3333333333334_q60_HIGH_RESOLUTION_crop-smart_subsampling-2_upscale.jpg>
    }
    """

    width_alias = '1-of-4'

    def setUp(self):
        super().setUp()
        self.dummy_plugin = mock.Mock(id=1)

        self.context = {
            'instance': self.dummy_plugin
        }
        self.image = FilerImageFactory()

    def test_context_default_values(self):
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('instance'), self.dummy_plugin)
        self.assertEqual(context.get('icon_enabled'), False)
        self.assertEqual(context.get('bg_enabled'), True)
        self.assertEqual(context.get('bg_color'), None)
        self.assertEqual(context.get('lazyload_enabled'), True)
        self.assertEqual(context.get('vh_enabled'), False)

    def test_context_ratio_values_xs(self):
        # 'xs': {'width': 450, 'ratio': '3-2'},
        w = 450
        h = w / 3 * 2

        expected_ration = '{}'.format(h / w * 100)  # 66.66666666666666
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('ratio_percent_sm'), '{}%'.format(expected_ration))
        self.assertEqual(context.get('ratio_vh_sm'), '{}vh'.format(expected_ration))

    def test_context_ratio_values_sm(self):
        # 'sm': {'width': 500, 'ratio': '3-2'},
        w = 500
        h = w / 3 * 2

        expected_ration = '{}'.format(h / w * 100)  # 66.66666666666666
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('ratio_percent_xs'), '{}%'.format(expected_ration))
        self.assertEqual(context.get('ratio_vh_xs'), '{}vh'.format(expected_ration))

    def test_context_ratio_values_xl(self):
        # 'xl': {'width': 500, 'ratio': '3-2'}
        w = 500
        h = w / 3 * 2

        expected_ration = '{}'.format(h / w * 100)  # 66.66666666666667
        context = render_image(self.context, self.image, width_alias=self.width_alias)

        self.assertEqual(context.get('ratio_percent_xl'), '{}%'.format(expected_ration))
        self.assertEqual(context.get('ratio_vh_xl'), '{}vh'.format(expected_ration))

    @mock.patch('allink_core.core.templatetags.allink_image_tags.get_thumbnailer', MockThumbnailer)
    def test_image_does_not_exist(self):
        """ if the image does not exist, no exception should not thrown """
        with mock.patch.object(MockThumbnailer, 'get_thumbnail') as mock_method:
            mock_method.side_effect = InvalidImageFormatError
            context = render_image(self.context, self.image, width_alias=self.width_alias)
            self.assertIsNone(context.get('thumbnail_xl'))

    @mock.patch('allink_core.core.templatetags.allink_image_tags.get_thumbnailer', MockThumbnailer)
    def test_thumbnail_options_default_values(self):
        # 'xl': {'width': 500, 'ratio': '3-2'}
        w = 500
        h = w / 3 * 2

        expected_thumbnail_options = {
            'crop': 'smart', 'bw': False, 'upscale': True, 'HIGH_RESOLUTION': True, 'zoom': None,
            'subject_location': self.image.subject_location, 'size': (w, h),
        }
        with mock.patch.object(MockThumbnailer, 'get_thumbnail') as mock_method:
            render_image(self.context, self.image, width_alias=self.width_alias)

            mock_method.assert_called_with(expected_thumbnail_options)
            self.assertEqual(mock_method.call_count, 3)


class ImageTagsImagePluginRenderTestCase(TestCase):
    """
    used width_alias:

    '1-of-4': {
        'xs': {'width': 450, 'ratio': '3-2'},
        'sm': {'width': 500, 'ratio': '3-2'},
        'xl': {'width': 500, 'ratio': '3-2'}
    },
    """

    def setUp(self):
        super().setUp()
        self.dummy_plugin = mock.Mock(id=1)
        self.context = {
            'instance': self.dummy_plugin
        }
        self.image = FilerImageFactory()
        self.sizes = {
            'xs': "450x{}".format(450 / 3 * 2),
            'sm': "500x{}".format(500 / 3 * 2),
            'xl': "500x{}".format(500 / 3 * 2),
        }

    def test_context_render_all_image_urls(self):
        context = Context({
            'instance': self.dummy_plugin,
            'image': self.image,

        })
        template_to_render = Template(
            '{% load allink_image_tags %}'
            '{% render_image image width_alias="1-of-4" %}'
        )
        rendered_template = template_to_render.render(context)

        for size in self.sizes.items():
            self.assertIn('{}__{}'.format(self.image.original_filename, size[1]), rendered_template)
