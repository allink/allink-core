# -*- coding: utf-8 -*-

__all__ = [
    'ALLINK_INSTALLED_APPS',
    'ALLINK_PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES',
    'ALLINK_CMS_PLACEHOLDER_CONF_PLUGINS',
    'ALLINK_LOCALE_PATHS',
    'ALLINK_PAGE_TOOLBAR_ENABLED',
    'ALLINK_MANDRILL_DEV_MODE',
    'ALLINK_MANDRILL_DEV_MODE_FROM_EMAIL_ADDRESS',
    'ALLINK_MANDRILL_DEV_MODE_TO_EMAIL_ADDRESSES',
    'ALLINK_CONTENT_PLUGIN_CHILD_CLASSES',
    'ALLINK_SEOACCORDION_PLUGIN_CHILD_CLASSES',
    'THUMBNAIL_QUALITY',
    'THUMBNAIL_OPTIMIZE_COMMAND',
    'DEBUG_TOOLBAR_CONFIG',
    'SOLO_CACHE_TIMEOUT',
]

####################################################################################

# Installed =Apps

ALLINK_INSTALLED_APPS = [
    # apps
    'debug_toolbar',
    'webpack_loader',
    'adminsortable',
    'sortedm2m',
    'solo',
    'import_export',
    'widget_tweaks',
    'lockdown',
    'reportlab',
    'djangocms_snippet',
    'djangocms_attributes_field',
    'django_countries',
    'django.contrib.postgres',
    'inline_static',

    # allink core apps
    'allink_core.core',
    'allink_core.core_apps.allink_categories',
    'allink_core.core_apps.allink_styleguide',
    'allink_core.core_apps.allink_legacy_redirect',

    'allink_core.core_apps.allink_quote',
    'allink_core.core_apps.allink_content',
    'allink_core.core_apps.allink_teaser',
    'allink_core.core_apps.allink_image',
    'allink_core.core_apps.allink_image_svg',
    'allink_core.core_apps.allink_gallery',
    'allink_core.core_apps.allink_video',
    'allink_core.core_apps.allink_social_icon',
    'allink_core.core_apps.allink_button_link',
    'allink_core.core_apps.allink_cms',
    'allink_core.core_apps.allink_seo_accordion',
    'allink_core.core_apps.allink_list_multicol',
]

####################################################################################

# =allink categories
# all models which use categories have to be listed here.
# the value has to be equal to "_meta.model_name"

ALLINK_PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES = [
    ('people', 'People'),
    ('news', 'News'),
    # ('locations', 'Locations'),
]

####################################################################################

# Assign Plugins to =Placeholders

# http://docs.django-cms.org/en/develop/reference/configuration.html#cms-placeholder-conf

ALLINK_CMS_PLACEHOLDER_CONF_PLUGINS = [
    'CMSAllinkContentPlugin',
    'CMSAllinkTeaserGridContainerPlugin',
    'Module',
    'CMSAllinkInfoBoxPlugin',
]

####################################################################################

# Assign Plugins which are allowed as child in Allink Content

ALLINK_CONTENT_PLUGIN_CHILD_CLASSES = [
    'TextPlugin',
    'SnippetPlugin',
    'AliasPlugin',
    # apps
    'CMSLocationsAppContentPlugin',
    'CMSPeopleAppContentPlugin',
    'CMSNewsAppContentPlugin',
    'CMSPartnerAppContentPlugin',
    # core
    'CMSAllinkTeaserPlugin',
    'CMSAllinkImagePlugin',
    'CMSAllinkImageSVGPlugin',
    'CMSAllinkGalleryPlugin',
    'CMSAllinkVideoEmbedPlugin',
    'CMSAllinkVideoFilePlugin',
    'CMSAllinkSocialIconContainerPlugin',
    'CMSAllinkButtonLinkContainerPlugin',
    # 'CMSAllinkPageChooserPlugin',
    'CMSAllinkLanguageChooserPlugin',
    'CMSAllinkSEOAccordionContainerPlugin',
    'CMSAllinkListMulticolPlugin',
    'CMSAllinkQuotePlugin',
]

####################################################################################

# Assign Plugins which are allowed as child in Allink SEO Accordion Content

ALLINK_SEOACCORDION_PLUGIN_CHILD_CLASSES = [
    'TextPlugin',
]

####################################################################################

# Locale

ALLINK_LOCALE_PATHS = [
    # project
    '/app/locale_extra',
    '/app/locale',
    # apps
    '/app/allink_core/apps/news/locale',
    '/app/allink_core/apps/config/locale',
    '/app/allink_core/apps/locations/locale',
    '/app/allink_core/apps/people/locale',
    '/app/allink_core/apps/partner/locale',
    # core
    '/app/allink_core/core/locale',
    # core_apps
    '/app/allink_core/core_apps/allink_categories/locale',
    '/app/allink_core/core_apps/allink_legacy_redirect/locale',
    '/app/allink_core/core_apps/allink_mandrill/locale',
    '/app/allink_core/core_apps/allink_styleguide/locale',
    '/app/allink_core/core_apps/allink_button_link/locale',
    '/app/allink_core/core_apps/allink_content/locale',
    '/app/allink_core/core_apps/allink_gallery/locale',
    '/app/allink_core/core_apps/allink_image/locale',
    '/app/allink_core/core_apps/allink_social_icon/locale',
    '/app/allink_core/core_apps/allink_video/locale',
    '/app/allink_core/core_apps/allink_cms/locale',
]

# ####################################################################################
#
# # Thumbnail

THUMBNAIL_QUALITY = 60

THUMBNAIL_OPTIMIZE_COMMAND = {
    'png': 'optipng {filename}',
    'gif': 'optipng {filename}',
    'jpeg': 'jpegoptim {filename}'
}


#  ####################################################################################
#
# # Debug Toolbar


def show_toolbar(request):
    return False


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

#  ####################################################################################
#
# # allink Page Extension

ALLINK_PAGE_TOOLBAR_ENABLED = False

#  ####################################################################################
#
# # allink E-Mail Mandrill
# if ALLINK_MANDRILL_DEV_MODE is set to True all emails will be sent to ALLINK_MANDRILL_DEV_MODE_TO_EMAIL_ADDRESSES
ALLINK_MANDRILL_DEV_MODE = True
ALLINK_MANDRILL_DEV_MODE_FROM_EMAIL_ADDRESS = 'test@allink.ch'
# we cant send to 'test@allink.ch' at the moment because of: https://support.google.com/a/answer/168383?hl=en
ALLINK_MANDRILL_DEV_MODE_TO_EMAIL_ADDRESSES = ['itcrowd@allink.ch', ]

#  ####################################################################################
#
# # cache
SOLO_CACHE_TIMEOUT = 60 * 60 * 24 * 180
