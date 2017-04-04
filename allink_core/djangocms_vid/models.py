# # -*- coding: utf-8 -*-
#
# from django.db import models
# from django.utils.translation import ugettext_lazy as _
# from django.utils.encoding import python_2_unicode_compatible
# from djangocms_attributes_field.fields import AttributesField
# from cms.models.pluginmodel import CMSPlugin
# from filer.fields.image import FilerImageField
#
# from allink_core.allink_base.models.choices import BLANK_CHOICE, RATIO_CHOICES
# from allink_core.allink_base.utils import get_additional_templates, get_additional_choices
# from allink_core.allink_base.models.model_fields import CMSPluginField
#
#
# @python_2_unicode_compatible
# class AllinkVidEmbedPlugin(CMSPlugin):
#     """
#     Renders an Iframe when ``link``
#     """
#
#     video_id = models.CharField(
#         verbose_name=_(u'Video ID'),
#         max_length=255,
#         help_text=_(u'Only provide the ID. The correct url will be automatically generated.'),
#     )
#     video_service = models.CharField(
#         _(u'Video Service'),
#         max_length=50,
#         choices=RATIO_CHOICES,
#         blank=True,
#         null=True
#     )
#     video_poster_image = FilerImageField(
#         verbose_name=_(u'Video Start Image'),
#         related_name="content_video_poster_image",
#         help_text=_(
#             u'This image is displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.'),
#         blank=True,
#         null=True
#     )
#     ratio = models.CharField(
#         _(u'Ratio'),
#         max_length=50,
#         choices=RATIO_CHOICES,
#         blank=True,
#         null=True
#     )
#     attributes = AttributesField(
#         verbose_name=_(u'Attributes'),
#         blank=True,
#     )
#
#     cmsplugin_ptr = CMSPluginField()
#
#     def __str__(self):
#         return self.label or self.embed_link or str(self.pk)
#
#     def copy_relations(self, oldinstance):
#         self.preview_image = oldinstance.preview_image
#
#     @classmethod
#     def get_ratio_choices(cls):
#         return BLANK_CHOICE + RATIO_CHOICES + get_additional_choices('RATIO_CHOICES')
#
#
# @python_2_unicode_compatible
# class AllinkVidFilePlugin(CMSPlugin):
#     """
#     is provided or the HTML5 <video> tag
#     """
#
#     video_file = FilerFileField(
#             verbose_name=_(u'Source'),
#             help_text=_(
#                 u'Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>Aspect ratio: TBD<br>File size: Dependent of video length. Generally speaking: Less is more.'),
#             blank=True,
#             null=True,
#             on_delete=models.SET_NULL,
#             related_name='content_video_file'
#         )
