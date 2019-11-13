# from cms.models import CMSPlugin
# from django.db import models
# from filer.fields.image import FilerImageField
#
#
# class AllinkQuotePlugin(CMSPlugin):
#     text = models.TextField(
#         'Quote Text',
#     )
#
#     author = models.CharField(
#         'Author Name',
#         max_length=255,
#         blank=True,
#         null=True
#     )
#
#     author_description = models.CharField(
#         'Author Description',
#         max_length=255,
#         blank=True,
#         null=True
#     )
#     author_image = FilerImageField("Author Image", blank=True)
#
#     def __str__(self):
#         return self.author
