# Changelog

Each release is divided into the following main categories:

- IMPORTANT: These changes might not be backward compatible and require updating existing code. (If not applied correctly your update will fail)
    - SETTINGS: change your setting.py accordingly
    - TEMPLATES: if templates form allink_core are overridden, you have to double apply these changes
    - URLS: changes to urls.py
    - REQUIREMENTS: new or changed requirements
    - DATA MIGRATIONS: stuff to migrate by hand or create data migrations manually
- NEW: New features or plugins
- FIXES: General bugfixes

## v0.0.9 (under development)

### IMPORTANT

###### SETTINGS
- Project Colors: The new markup of the `PROJECT_COLORS` settings is as followed and requires to be updated:
    ```python
    PROJECT_COLORS = {
        '#c6c6c6': 'project-color-1', # color
        '#eceeef': 'project-color-2', # color
        '#f7f7f9': 'project-color-3', # color
    }
    ```
- lockdown introduced. add the following:
    ```python
    ####################################################################################

    # =Lockdown

    if DEBUG:
        LOCKDOWN_ENABLED = False
    LOCKDOWN_PASSWORDS = ('stage', )
    ```
- We want to keep HTML comments (because of the allink ad in the source code):
    ```python
    ####################################################################################

    # =HTML Minifier

    KEEP_COMMENTS_ON_MINIFYING = True

    ```
- Fix the SENTRY_DSN (change 'DNS' to 'DSN' !!) -> also change this in environment variables
- LOCALE_PATHS introduced
    ```python
    LOCALE_PATHS = ALLINK_LOCALE_PATHS

    ```
- refactoring TEMPLATES settings:
    ```python
    ####################################################################################

    context_processors = TEMPLATES[0].get('OPTIONS', {}).get('context_processors', [])
    context_processors.extend([
        'django.template.context_processors.request',
        'allink_core.allink_config.context_processors.allink_config',
        'allink_apps.config.context_processors.config',
    ])

    ```

###### TEMPLATES

###### URLS

###### REQUIREMENTS

- Add the following packages:
```
django-lockdown==1.4.2
django-htmlmin==0.10.0
```

###### DATA MIGRATIONS

- when making migrations for allink_apps on project basis, it's important, that "active" gets renamed to "is_active".
  The field should not be deleted and created with new name, else all data gets lost.

###### DOCKERFILE
- djangocms_vid is now able to read dimensions of video for disaplying appropriate preview image. add to Dockerfile:
    ```python
    # additional requirements
    # -------------------
    RUN apt-get update && \
        apt-get install libav-tools -y --force-yes --no-install-recommends
    ```

### NEW

- Image Template: `bg_color` is now supported when setting a background color for an image inside a column or via templatetag `render_app_content_image_detail` or `render_app_content_image` by setting e.g. `bg_color=1`
- Content Plugin: The inner container background image is now handled with a separate HTML-element that allows us to stack the image and the overlay text on small screens. Requires the latest static core.
- field "active" from AllinkBaseModel renamed to "is_active"
- HTML gets minified
- BUTTON_LINK_PLUGIN_PROJECT_CSS_CLASSES introduced
- All colors use now the colorfield with colorpicker widget
- Mailchimp CMS plugin
- locale folders in app directories

### FIXES

- Gallery: Ratio option `original` has been removed (but left for Image Plugin)
- Button Link Plugin: Link target are now respected in the template.
- Members: Views are customised. Ajax forms now working
- Base Model: Separated filter and categories fieldsets, applied default ordering on querysets
- Base Model & Mixins: Fixed querset filter & ordering distinct bug
- fix empty result template when object_list is a list


## v0.0.8

### IMPORTANT
  python 3 compatibility

###### SETTINGS
- major changes regarding content plugin wrapper: every app plugin requires an content plugin now. there are two options:
    -> change project specific app to be added to content plugin children (not placeholder `ALLINK_CMS_PLACEHOLDER_CONF_PLUGINS` anymore) -> `CMS_ALLINK_CONTENT_PLUGIN_CHILD_CLASSES.extend(..)`
    1. migrate by hand every app plugin so that it is wrapped inside a content_pluin (no further changes to settings or templates necessary.)
    2. dont migrate by hand. and continue to add app plugins directly.
        - you have to add and rename the file form core `app_content/app_content_base_legacy.html` file to your project templates folder: `app_content/app_content_base.html`:
        - you have to add in the settings:
        ```python
        # this project handles every app_plugin separately and doesn't require an
        # allink_content_plugin wrapper. So the placeholder settings have to be overidden here.
        # also notice the project specific template "app_content/app_content_base.html"
        ALLINK_CMS_PLACEHOLDER_CONF_PLUGINS.extend([
            'CMSLocationsPlugin',
            'CMSPeoplePlugin',
            'CMSWorkPlugin',
            'CMSBlogPlugin',
            'CMSTestimonialPlugin'
        ])
        TO_REMOVE = [
            'CMSLocationsPlugin',
            'CMSPeoplePlugin',
            'CMSWorkPlugin',
            'CMSBlogPlugin',
            'CMSTestimonialPlugin'
        ]
        CMS_ALLINK_CONTENT_PLUGIN_CHILD_CLASSES = [item for item in CMS_ALLINK_CONTENT_PLUGIN_CHILD_CLASSES if item not in TO_REMOVE]
        ```

            - you have to add and rename the file form core `app_content/app_content_base_legacy.html` file in your project templates folder: `app_content/app_content_base.html`:



###### TEMPLATES

###### URLS

###### REQUIREMENTS

###### DATA MIGRATIONS


### NEW

- allink_categories: After adding a root category redirect to edit page for model_names option.
- extra_css_classes removed from admin
- djangocms_vid_file and djangocms_vid_embed implemented (dropped djangocms_video)(project css classes: VID_PLUGIN_PROJECT_CSS_CLASSES)
- djangocms_image now supports project css classes (IMAGE_PLUGIN_PROJECT_CSS_CLASSES), and bg_color
- Content Plugin: Support for vertical alignment of columns added (the tallest element defines the boundaries). Important: Requires at least `allink-core-static` commit `1256fa94cdc7b3ba8f6b48be384171e305e03ad5`
- config: New app added in allink_apps. A migrations folder (`allink_apps_migrations.config`) is necessary in every project after this version.
- Buttons and Image links can now link on all internal app sites
- Button/Link Plugin: Admin modal: Link settings are now expanded per default.
- button_link_plugin: page_link to internal_link, migration 0022
- image_plugin:  page_link to internal_link, migration 0014

### FIXES

- Mailchimp Forms: `signup_form.html` and `signup_form_advanced.html` now have their own extendable `base` templates with numerous `blocks` that can be overwritten on a project basis.
- Button Link Plugin: Type `link` links now get the class `text`.

## v0.0.7

### IMPORTANT

###### SETTINGS
- contacts migration folder was added to allink_settings, so you have to create a folder `contact` (and create an empty `__init__.py` in it [ha!]) within `apps/allink_apps_migrations`. If you already have migrated contacts you have to manually copy all migrations to the app specific folder.
- new setting PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES must be added by core update.
```python
# all models which can be used as tag for categories.
# all categories with the same tag can be used
# in a filter on a plugin.
# the value has to be equal to "_meta.model_name"
PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES = [
    ('locations', 'Locations'),
]
```

###### TEMPLATES

###### URLS

###### REQUIREMENTS
- djangocms-helper==0.9.8
- coverage==4.3.4

###### DATA MIGRATIONS

### NEW
- allink_apps: galleries not on app anymore, instead the gallery on detail page is added with GalleryPlugin
- Plugin overview pages can be filterd over dropdowns by Foreingkey- and Char-Fields
    - Hint for updates: keyword argument `filter` in methode `get_render_queryset_for_display` on `BlogAppContentPlugin` must be renamed to `filters`
- allink_categories: model_categories can be defined on child and/or parent.
- allink_categories: categories can get generated from other apps, an get a tag. Like this when using an ajax filter by category, only categories generated from a specific model can be choosen.
- allink_apps: App Plugins now support AND operator for filtering categories
- allink_apps: get_absolute_urlallow now language as parameter
- Content Plugin: The template `content.html` can now be overwritten on a project basis with the following required content `{% extends "djangocms_content/content_base.html" %}`. Afterwards blocks can be set.
- AllinkCategories are now just defined for parent category (creating a new cagetory has to be a two step process. First create, if new root than, tag it with the model_name)
- App Content Plugin: The template `app_content_base.html` now has a new block `app_content_load_more_btn_class_container` with which the load more button can be turned into a link by defining an empty block.
- basic tests for allink_apps.work added

### FIXES
- Bugfix in djangocms_instagram: Added queryset length when no display option with paginated_by value


## v0.0.6

### IMPORTANT

###### SETTINGS
- PROJECT_COLORS is now a tuple and not a list anymore:
```python
PROJECT_COLORS = (
    ('project-color-1', 'Project Color 1'),
    ('project-color-2', 'Project Color 2'),
    ('project-color-3', 'Project Color 3'),
)
```
- CMS_PLACEHOLDER_CONF was supplemented with the placeholder fields from allink_apps
- members migration folder was added to allink_settings, so you have to create a folder (with "__init__.py") in apps/allink_apps_migrations.

###### TEMPLATES
- new templates:
   - `admin/submit_line.html`
   - `admin/change_form.html`
   - `accounts/...`
- modificaton in `base_root.html` (new tag favicons)
- modification in every plugin template form allink_apps `object.show_detail_link` introduced.
- allink_config: `base_title` and `og_image` in `base_root.html`.


###### URLS
- debug_toolbar urls added
- contact urls added

###### REQUIREMENTS
- new
    - django-polymorphic==0.8.1
    - django-debug-toolbar==1.7

###### DATA MIGRATIONS
- allink_legacy_redirect has to be manually migrated because migration '0006_auto_20170320_0702' was not working correctly.
- blog: datamigrations blog polymorphic (see data migrations as reference [file](https://www.google.com))
- blog: detail placeholderfield datamigrations
- djangocms_image: (danach djangocms_picture delete table contents and uninstall

### NEW

- Instagram Plugin: Initial release
- Content Plugin: Utility blocks added to default `content.html` that now can be extended on a project basis.
- Content Plugin: Empty columns now get the class `col-empty` and are set to `display:none;` by default on mobile devices.
- Content Plugin: Support for column ordering (for mobile only) has been added. Requires the latest `allink-core-static`.
- Allink Legacy Redirects: Redirects for legacy URLs with GET parameters consider the parameters.

### FIXES

- Button/Link Plugin: CSS classes are now set.
- Button/Link Plugin: Admin modal: Link settings are now expanded per default.
- Button/Link Plugin: `get_link_special_choices` has now a blank default value.
