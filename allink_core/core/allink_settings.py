# -*- coding: utf-8 -*-
from aldryn_addons.utils import senv
from django.conf import settings
####################################################################################

# Installed =Apps

ALLINK_INSTALLED_APPS = [
    # apps
    'debug_toolbar',
    'allauth',
    'allauth.account',
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

    # allink core apps
    'allink_core.core',
    'allink_core.core_apps.allink_seo',
    'allink_core.core_apps.allink_categories',
    'allink_core.core_apps.allink_mailchimp',
    'allink_core.core_apps.allink_styleguide',
    'allink_core.core_apps.allink_legacy_redirect',
    'allink_core.core_apps.allink_terms',

    'allink_core.core_apps.allink_content',
    'allink_core.core_apps.allink_image',
    'allink_core.core_apps.allink_gallery',
    'allink_core.core_apps.allink_video',
    'allink_core.core_apps.allink_social_icon',
    'allink_core.core_apps.allink_button_link',
    'allink_core.core_apps.allink_group',
    'allink_core.core_apps.allink_instagram',
    'allink_core.core_apps.allink_pdf',
    'allink_core.core_apps.allink_cms',
    'allink_core.core_apps.allink_icon',
]

####################################################################################

# =allink categories
# all models which use categories have to be listed here.
# the value has to be equal to "_meta.model_name"

ALLINK_PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES = [
    ('people', 'People'),
    ('work', 'Work'),
    ('testimonial', 'Testimonials'),
    ('news', 'News'),
    ('events', 'Events'),
    # ('locations', 'Locations'),
]

####################################################################################

# Assign Plugins to =Placeholders

# http://docs.django-cms.org/en/develop/reference/configuration.html#cms-placeholder-conf

ALLINK_CMS_PLACEHOLDER_CONF_PLUGINS = [
    'CMSAllinkContentPlugin',
]

####################################################################################

# Assign Plugins which are allowed as child in Allink Content

CMS_ALLINK_CONTENT_PLUGIN_CHILD_CLASSES = [
    'TextPlugin',
    'SnippetPlugin',
    'AliasPlugin',
    # apps
    'CMSLocationsAppContentPlugin',
    'CMSPeopleAppContentPlugin',
    'CMSWorkAppContentPlugin',
    'CMSNewsAppContentPlugin',
    'CMSEventsAppContentPlugin',
    'CMSTestimonialsAppContentPlugin',
    # search
    'CMSWorkSearchPlugin',
    # core
    'CMSAllinkTermsPlugin',
    'CMSAllinkImagePlugin',
    'CMSAllinkGalleryPlugin',
    'CMSAllinkVideoEmbedPlugin',
    'CMSAllinkVideoFilePlugin',
    'CMSAllinkSocialIconContainerPlugin',
    'CMSAllinkSignupFormPlugin',
    'CMSAllinkButtonLinkContainerPlugin',
    'CMSAllinkGroupContainerPlugin',
    'CMSAllinkInstagramPlugin',
    'CMSAllinkContactRequestPlugin',
    'CMSAllinkPageChooserPlugin',
    'CMSAllinkIconPlugin'
]
####################################################################################

# Middlewareclassss

ALLINK_MIDDLEWARE_CLASSES = [
    'lockdown.middleware.LockdownMiddleware',
    'allink_core.core.middleware.AllinkUrlRedirectMiddleware',
    'allink_core.core_apps.allink_legacy_redirect.middleware.AllinkLegacyRedirectMiddleware',
]

####################################################################################

# Locale

ALLINK_LOCALE_PATHS = [
    # project
    '/app/locale_extra',
    '/app/locale',
    # apps
    '/app/allink_core/apps/news/locale',
    '/app/allink_core/apps/events/locale',
    '/app/allink_core/apps/config/locale',
    '/app/allink_core/apps/contact/locale',
    '/app/allink_core/apps/locations/locale',
    '/app/allink_core/apps/members/locale',
    '/app/allink_core/apps/people/locale',
    '/app/allink_core/apps/testimonials/locale',
    '/app/allink_core/apps/work/locale',

    # '/app/allink_apps/news/locale',
    # '/app/allink_apps/events/locale',
    # '/app/allink_apps/config/locale',
    # '/app/allink_apps/contact/locale',
    # '/app/allink_apps/locations/locale',
    # '/app/allink_apps/members/locale',
    # '/app/allink_apps/people/locale',
    # '/app/allink_apps/testimonials/locale',
    # '/app/allink_apps/work/locale',

    # core
    '/app/allink_core/core/locale',
    # core_apps
    '/app/allink_core/core_apps/allink_categories/locale',
    '/app/allink_core/core_apps/allink_seo/locale',
    '/app/allink_core/core_apps/allink_legacy_redirect/locale',
    '/app/allink_core/core_apps/allink_mailchimp/locale',
    '/app/allink_core/core_apps/allink_mandrill/locale',
    '/app/allink_core/core_apps/allink_styleguide/locale',
    '/app/allink_core/core_apps/allink_button_link/locale',
    '/app/allink_core/core_apps/allink_content/locale',
    '/app/allink_core/core_apps/allink_gallery/locale',
    '/app/allink_core/core_apps/allink_group/locale',
    '/app/allink_core/core_apps/allink_image/locale',
    '/app/allink_core/core_apps/allink_instagramm/locale',
    '/app/allink_core/core_apps/allink_social_icon/locale',
    '/app/allink_core/core_apps/allink_video/locale',
    '/app/allink_core/core_apps/allink_pdf/locale',
    '/app/allink_core/core_apps/allink_cms/locale',
    '/app/allink_core/core_apps/allink_icon/locale',
]


# ####################################################################################
#
# # Thumbnail

THUMBNAIL_QUALITY = 85

THUMBNAIL_OPTIMIZE_COMMAND = {
    'png': 'optipng {filename}',
    'gif': 'optipng {filename}',
    'jpeg': 'jpegoptim {filename}'
}

#  ####################################################################################
#
# # Debug Toolbar

def show_toolbar(request):
    return senv('DEBUG_TOOLBAR_ENABLED', False)


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}