####################################################################################

# Installed =Apps

ALLINK_INSTALLED_APPS = [
    # apps
    'webpack_loader',
    'adminsortable',
    'sortedm2m',
    'solo',
    'import_export',
    'cmsplugin_form_handler',

    # allink core apps
    'allink_core.allink_base',
    'allink_core.allink_config',
    'allink_core.allink_categories',
    'allink_core.allink_mailchimp',
    'allink_core.allink_styleguide',

    # allink apps
    'allink_apps.locations',
    'allink_apps.people',
    'allink_apps.work',
    'allink_apps.testimonials',
    'allink_apps.blog',

    # allink core djangocms plugins
    'allink_core.djangocms_content',
    'allink_core.djangocms_gallery',
    'allink_core.djangocms_socialicon',
    'allink_core.djangocms_button_link',

]

####################################################################################

# = allink categories
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
    'CMSLocationsPlugin',
    'CMSPeoplePlugin',
    'CMSWorkPlugin',
    'CMSBlogPlugin',
    'CMSTestimonialPlugin'
]
