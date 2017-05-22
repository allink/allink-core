# -*- coding: utf-8 -*-
from aldryn_addons.utils import senv

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
    'cmsplugin_form_handler',
    'widget_tweaks',
    'lockdown',
    'reportlab',
    'djangocms_snippet',

    # allink core apps
    'allink_core.allink_base',
    'allink_core.allink_config',
    'allink_core.allink_categories',
    'allink_core.allink_mailchimp',
    'allink_core.allink_styleguide',
    'allink_core.allink_legacy_redirect',
    'allink_core.allink_terms',

    # allink apps
    'allink_apps.members',
    'allink_apps.locations',
    'allink_apps.people',
    'allink_apps.work',
    'allink_apps.blog',
    'allink_apps.testimonials',
    'allink_apps.contact',
    'allink_apps.config',

    # allink core djangocms plugins
    'allink_core.djangocms_content',
    'allink_core.djangocms_image',
    'allink_core.djangocms_gallery',
    'allink_core.djangocms_vid',
    'allink_core.djangocms_socialicon',
    'allink_core.djangocms_button_link',
    'allink_core.djangocms_group',
    'allink_core.djangocms_instagram',

]

####################################################################################

# =Migration Modlues allink apps
ALLINK_MIGRATION_MODULES = {
    'blog': 'apps.allink_apps_migrations.blog',
    'locations': 'apps.allink_apps_migrations.locations',
    'people': 'apps.allink_apps_migrations.people',
    'testimonials': 'apps.allink_apps_migrations.testimonials',
    'work': 'apps.allink_apps_migrations.work',
    'members': 'apps.allink_apps_migrations.members',
    'contact': 'apps.allink_apps_migrations.contact',
    'config': 'apps.allink_apps_migrations.config',
}

####################################################################################

# =allink categories
# all models which use categories have to be listed here.
# the value has to be equal to "_meta.model_name"

ALLINK_PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES = [
    ('people', 'People'),
    ('work', 'Work'),
    ('testimonial', 'Testimonials'),
    ('blog', 'Blog'),
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
    # apps
    'CMSLocationsPlugin',
    'CMSPeoplePlugin',
    'CMSWorkPlugin',
    'CMSBlogPlugin',
    'CMSTestimonialPlugin',
    # core
    'CMSAllinkTermsPlugin',
    'CMSAllinkImagePlugin',
    'CMSAllinkGalleryPlugin',
    'CMSAllinkVidEmbedPlugin',
    'CMSAllinkVidFilePlugin',
    'CMSAllinkSocialIconContainerPlugin',
    'CMSAllinkSignupFormPlugin',
    'CMSAllinkButtonLinkContainerPlugin',
    'CMSAllinkGroupContainerPlugin',
    'CMSAllinkInstagramPlugin',
    'CMSAllinkContactRequestPlugin'

]
####################################################################################

# Middlewareclassss

ALLINK_MIDDLEWARE_CLASSES = [
    'lockdown.middleware.LockdownMiddleware',
    'allink_core.allink_base.utils.middleware.AllinkUrlRedirectMiddleware',
    'allink_core.allink_legacy_redirect.middleware.AllinkLegacyRedirectMiddleware',
]

####################################################################################

# Locale

ALLINK_LOCALE_PATHS = [
    '/app/locale',
    # apps
    '/app/allink_apps/blog/locale',
    '/app/allink_apps/config/locale',
    '/app/allink_apps/contact/locale',
    '/app/allink_apps/locations/locale',
    '/app/allink_apps/members/locale',
    '/app/allink_apps/people/locale',
    '/app/allink_apps/testimonials/locale',
    '/app/allink_apps/work/locale',

    '/app/allink_core/allink_base/locale',
    '/app/allink_core/allink_categories/locale',
    '/app/allink_core/allink_config/locale',
    '/app/allink_core/allink_legacy_redirect/locale',
    '/app/allink_core/allink_mailchimp/locale',
    '/app/allink_core/allink_mandrill/locale',
    '/app/allink_core/allink_styleguide/locale',
    '/app/allink_core/djangocms_button_links/locale',
    '/app/allink_core/djangocms_content/locale',
    '/app/allink_core/djangocms_gallery/locale',
    '/app/allink_core/djangocms_group/locale',
    '/app/allink_core/djangocms_image/locale',
    '/app/allink_core/djangocms_instagramm/locale',
    '/app/allink_core/djangocms_socialicon/locale',
    '/app/allink_core/djangocms_vid/locale',
]


# ####################################################################################
#
# # Debug Toolbar

def show_toolbar(request):
    return senv('DEBUG_TOOLBAR_ENABLED', False)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
