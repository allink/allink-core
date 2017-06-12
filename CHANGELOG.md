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

## v0.0.10 (under development)

### IMPORTANT
- The following dependencies/plugins have been removed from the core. Unregister them accordingly:

    ```python
    from cms.plugin_pool import plugin_pool
    from djangocms_file.cms_plugins import FilePlugin, FolderPlugin
    from djangocms_picture.cms_plugins import PicturePlugin

    plugin_pool.unregister_plugin(PicturePlugin)

    # Unregister existing Plugins

    plugin_pool.unregister_plugin(FilePlugin)
    plugin_pool.unregister_plugin(FolderPlugin)
    ```

### IMPORTANT (SPEZIALE): Webpack Loader Update

When Updating the `allink-core`, it is <strong>required</strong> to go through the following steps in order to make sure that the compiled static files are loaded correctly.

Additionally, project specific plugins require the `class Media` (described below) imports to be updated, too.

- Update requirements to `django-webpack-loader==0.5.0`
- execute:
    - npm i/ npm run dev
    - docker stop $(docker ps -a -q)
- django-webpack-loader: Static assets (dev and production (with hashes)) for CKEDITOR and CMSPlugins are now being loaded via django-webpack-loader.
  To load the project styles in CKEDITOR add the following code to your project's `settings.py` (update `CKEDITOR_SETTINGS.contentsCss`):
  ```python
  from webpack_loader.utils import get_files

  ...

  CKEDITOR_SETTINGS = {
      'contentsCss': get_files('app')[1]['publicPath'],
  ```
- `base_root.html` template (project specific): The bundle names in `webpack.config.js` have been updated. There now are only two bundles, `app` and `djangocms_custom_admin`. The `render_bundle` template tags must be updated like this:

  ```html
  <!-- head -->
  {% render_bundle 'app' 'css' %}

  <!-- body -->
  {% render_bundle 'app' 'js' %}
    ```

- `webpack.config.js`: Replace exisiting `entry` with the following code:
  ```JS
  entry: {
      app: [
          PATHS.app,
          PATHS.style,
      ],
      djangocms_custom_admin: [
          PATHS.djangocms_custom_admin_style,
          PATHS.djangocms_custom_admin_scripts,
      ]
  },
  ```

- `webpack/lib.js`: Make sure that hashing is enabled in `production`:
  ```JS
  output: {
      filename: '[name].min.[hash].js',
  },

  new ExtractTextPlugin('[name].min.[hash].css'),
  ```

  If you are experiencing issues while updating the project, try running `npm run dev` so that the new bundles `app` and `django_custom_admin` exist.

- django-webpack-loader: All core plugins have been updated to load static assets via `django-webpack-loader`. If you need `djangocms_custom_admin_scripts` or `djangocms_custom_admin_style` in a new plugin add the following code to the admin.py / cms_plugins.py
  ```python
  from webpack_loader.utils import get_files

  ...

  class Media:
      js = (
          get_files('djangocms_custom_admin')[0]['publicPath'],
      )
      css = {
          'all': (
              get_files('djangocms_custom_admin')[1]['publicPath'],

          )
      }
  ```
###### SETTINGS
-  import from allink_settings -> DEBUG_TOOLBAR_CONFIG
-  we refactored the whole image tags. the new tag 'render_image' requires a dict in the settings (when updating it is crucial, that you specify the project image ratios in the corresponding with_alias!)
   this is important, mainly for all the images added with the image plugin. All the images in the context of app-templates (detail, and plugins) will still use the old THUMBNAIL_ALIASES
    ```python
    ##############################################

    # =Thumbnail

    THUMBNAIL_HIGHRES_INFIX = '_2x'

    ####################################################################################

    # =Thumbnail width aliases

    THUMBNAIL_WIDTH_ALIASES = {
        '1-of-1': {
            'xs': {'width': 450, 'ratio': '3-2'},
            'sm': {'width': 1200, 'ratio': '3-2'},
            'xl': {'width': 1500, 'ratio': '3-2'}
        },
        '1-of-2': {
            'xs': {'width': 450, 'ratio': '3-2'},
            'sm': {'width': 650, 'ratio': '3-2'},
            'xl': {'width': 800, 'ratio': '3-2'}
        },
        '2-of-3': {
            'xs': {'width': 450, 'ratio': '3-2'},
            'sm': {'width': 900, 'ratio': '3-2'},
            'xl': {'width': 1200, 'ratio': '3-2'}
        },
        '1-of-3': {
            'xs': {'width': 450, 'ratio': '3-2'},
            'sm': {'width': 500, 'ratio': '3-2'},
            'xl': {'width': 500, 'ratio': '3-2'}
        },
        '1-of-4': {
            'xs': {'width': 450, 'ratio': '3-2'},
            'sm': {'width': 500, 'ratio': '3-2'},
            'xl': {'width': 500, 'ratio': '3-2'}
        },
        '1-of-5': {
            'xs': {'width': 450, 'ratio': '3-2'},
            'sm': {'width': 400, 'ratio': '3-2'},
            'xl': {'width': 400, 'ratio': '3-2'}
        },
        '1-of-6': {
            'xs': {'width': 450, 'ratio': '3-2'},
            'sm': {'width': 400, 'ratio': '3-2'},
            'xl': {'width': 400, 'ratio': '3-2'}
        }
    }

    ```
- The new LinkField needs to know, which apps to use to generate link choices with some details:
    ```python
    PROJECT_LINK_APPHOOKS = OrderedDict([
        ('Page', []),  # Not Apphook but linkable
        ('NewsApphook', {'detail': ('allink_apps.blog.models.News', ['slug'])}), # Linkable urls (urlnames): (ModelName, [url_parameters])
        ('EventsApphook', {'detail': ('allink_apps.blog.models.Events', ['slug'])}),
        ('LocationsApphook', {'detail': ('allink_apps.locations.models.Locations', ['slug'])}),
        ('MembersApphook', {'detail': ('allink_apps.members.models.Members', ['slug'])}),
        ('PeopleApphook', {'detail': ('allink_apps.people.models.People', ['slug'])}),
        ('TestimonialsApphook', {'detail': ('allink_apps.testimonials.models.Testimonial', ['slug'])}),
        ('WorkApphook', {'detail': ('allink_apps.work.models.Work', ['slug'])}),
    ])
    ```
- remove 'django.middleware.cache.UpdateCacheMiddleware' and django.middleware.cache.FetchFromCacheMiddleware' (because they cache all responses from views, e.g AllinkBaseDetailView)
- rename all PROJECT_CSS_CLASSES:
    PROJECT_CSS_CLASSES -> CONTENT_CSS_CLASSES
    BUTTON_LINK_PLUGIN_PROJECT_CSS_CLASSES -> BUTTON_LINK_CSS_CLASSES
    IMAGE_PLUGIN_PROJECT_CSS_CLASSES -> IMAGE_CSS_CLASSES
- TIME_ZONE ='Europe/Zurich' (careful when date/time critical content)
- now the templates for all app plugins have to be specified in the settings!
     ```python
    ####################################################################################

    # =allink app_content additional templates for apps
    # the variable name prefix 'PEOPLE' in 'PEOPLE_PLUGIN_TEMPLATES' has to be equal to "_meta.model_name"
    # default templates are (these exist as templates in allink_base dir):
    #     ('grid_static', 'Grid (Static)'),
    #     ('grid_dynamic', 'Grid (Dynamic)'),
    #     ('list', 'List'),
    #     ('slider', 'Slider'),
    #     ('table', 'Table'),

    BLOG_PLUGIN_TEMPLATES = (
        ('grid_static', 'Grid (Static)'),
        ('list', 'List'),
        ('slider', 'Slider'),
    )

    LOCATIONS_PLUGIN_TEMPLATES = (
        ('grid_static', 'Grid (Static)'),
        ('map', 'Map'),
    )

    PEOPLE_PLUGIN_TEMPLATES = (
        ('grid_static', 'Grid (Static)'),
        ('list', 'List'),
        ('list_variation', 'List (Horizontal)'),
        ('grid_static_variation', 'Grid (Static) - without contact details'),
        # ('grid_random', 'Grid (Random)'),
    )

    TESTIMONIAL_PLUGIN_TEMPLATES = (
        ('grid_static', 'Grid (Static)'),
        ('grid_dynamic', 'Grid (Dynamic)'),
        ('slider', 'Slider'),
    )

    WORK_PLUGIN_TEMPLATES = (
        ('grid_static', 'Grid (Static)'),
        ('grid_dynamic', 'Grid (Dynamic)'),
        ('list', 'List'),
        ('slider', 'Slider'),
    )

    ####################################################################################
    #  =other templates which are defined in settings

    INSTAGRAM_PLUGIN_TEMPLATES = (
        ('grid_static', 'Grid (Static)'),
    )

    GALLERY_PLUGIN_TEMPLATES = (
        ('slider', 'Slider'),
        ('grid_random', 'Grid (Random)'),
    )

    # ADDITIONAL_CONTENT_PLUGIN_TEMPLATES = (
        # ('col-7', '7 Columns', 7, 'col-1-of-7'),
    # )

    ADDITIONAL_BLOG_DETAIL_TEMPLATES = (
        ('with_header', 'With lead section'),
    )

    ```

###### TEMPLATES
- people job_function (which it was used in tejakob for example) was substitutett with property 'units'. You now have to add categories (with unit=True) and tag th person with it. this allowes us to categories people without having to maintain both fields 'unit' and categories
- meta block in base_root.html  (also every app template)

###### URLS

###### REQUIREMENTS
- djangocms-snippet==1.9.2
- beautifulsoup4==4.6.0
- reportlab==3.4.0

###### DATA MIGRATIONS
- update with caution in projects whcih still use inline images to display galleries (hdf, mfgz, ..?) we added a field preview_image (not a property anymore) the galleries are now added as a plugin inside the content_palceholder
 -> and if you update make sure you migrate the images! (see data_migrations/0017_migrate_preview_image.py)

- Color Picker: Fields using the colorpicker (bg_color) need to be migrated. Therfore replace the hex-value in the databaseco with the project color name as defined in SETTINGS

- Legacy Links: Migration for new LinkField. Warnings in Console for Links which can't be migrated automatically. maybe the dependancies must be ajusted on project base (Migration 0012)
- Button Link Plugin: Migration for new LinkField. Warnings in Console for Links which can't be migrated automatically. maybe the dependancies must be ajusted on project base (Migration 0028)
- Image Plugin: Migration for new LinkField. Warnings in Console for Links which can't be migrated automatically. maybe the dependancies must be ajusted on project base (Migration 0026)

### NEW
- debug toolbar installed manually, because debug toolbar is extremly slow we disable it by default (to enable it, just set DEBUG_TOOLBAR_ENABLED=True in the env variables.)
- new tuple PROJECT_CATEGORY_IDENTIFIERS: allowes you to specify a uique identifier, from wich you can navigae back from a app model (e.g to get the category name for the Units (categories) a person is tagged with.)
- allink_config: Field for google_site_verification code added, because verification through tag manager snippet does not work anymore
- LinkField: Internal Links are handled through new AllinkInternalLinkFieldsModelMixin, AllinkInternalLinkFieldMixin and SelectLinkField
- LinkField integrated in allink_legacy_redirect, djangocms_image and djangocms_button_link
- djangocms_gallery: added fullscreen & counter flags. Additional markup in `base_root.html` (before end of body) and custom styles are needed.
  ```html
  <div class="swiper-fullscreen-container">
      <a href="#" class="swiper-button-fullscreen-close" data-softpage-disabled data-close-swiper-fullscreen>
          <i class="sr-only" lang="en">
              {% trans "Close" %}
          </i>
      </a>
      <div class="swiper-fullscreen"></div>
  </div>

  ```

- djangocms_pdf was added (enables manual page breaks in pdf export) -> to enable CMSAllinkPageBreakPlugin in a certain placeholder ad just add it in the settings.py
- render_meta_og was introduced to render meta tags
- djangocms_gallery: Added autoplay disable option (default is true). Important: Requires at least `allink-core-static` commit `f8e9b17c21dec85a7f506945783e39a9ad906764`.
  Additional markup is needed on `swiper-default` tag like in `slider/content.html` for example:
  ```html
  <div class="swiper-container swiper-default swiper-gallery-plugin" {% if instance.auto_start_enabled == False %}data-autoplay="false"{% endif %}>
  ...
  </div>
  ```
- ButtonLinkPlugin: Added additional email fields subject and body text
- placeholder_has_content: allink_cms_tags template tag that renders boolean to variable if placeholder has plugins or not
  ```html
  {% load allink_cms_tags %}
  {% placeholder_has_content object.header_placeholder as header_has_content %}
  <div class="content-section {% if not header_has_content %}hidden{% endif %}"></div>
  ```


### FIXES

## v0.0.9

### IMPORTANT

###### SETTINGS
- Project Colors: The new markup of the `PROJECT_COLORS` settings is as followed and requires to be updated (the colors in allink_config have to b emanually set to the project colors defined in the settings.):
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
- BUTTON_LINK_CSS_CLASSES introduced
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
- djangocms_image now supports project css classes (IMAGE_CSS_CLASSES), and bg_color
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
