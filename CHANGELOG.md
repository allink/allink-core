# Changelog
The information for each release is divided into the following chapters:

#### IMPORTANT
These changes might not be backward compatible and require updating existing code. (If not applied correctly your update will fail)
###### SETTINGS
change your setting.py accordingly
###### TEMPLATES
if templates from allink_core are overridden, you have to apply these changes as well in the project templates.
###### URLS
changes to urls.py
###### REQUIREMENTS
new or changed requirements
###### DATA MIGRATIONS
stuff to migrate by hand or create data migrations manually
#### NEW
new features or plugins
#### FIXES
general bugfixes

## v2.8.0
#### IMPORTANT

- Removed ```AllinkAddressFieldsModel``` from models/fields_model.py
    - All Fields have been moved directly to BaseLocations and BasePeople
    - If you have a project specific model which inherits from ```AllinkAddressFieldsModel``` you also have to put the fields directly into that model
    - Hint: search for ```AllinkAddressFieldsModel``` and make sure it's not part of the project specific files

- Added load_more_internallink to AppContentPlugin.
    - add following code to ```models.py``` on each project based app within  
    ```class APP_NAMEAppContentPlugin(AllinkBaseAppContentPlugin)``` (replace APP_LABEL with actual app label):
        ```
        load_more_internallink = PageField(
            verbose_name='Custom Load More Link',
            help_text='Link for Button Below Items if custom URL is chosen',
            related_name="load_more_internallink_APP_LABEL",
            blank=True,
            null=True,
        )
        ```
    - hint: search for ```apphook_page = PageField``` and place below in all model files.
    - run migrations

- added teaser_link_url field on all models that have a teaser
    -  To take advantage of these changes you must add `teaser_link_url=object.teaser_dict.teaser_link_url` to all 
    overridden item templates which use a teaser via include of teaser tile such as news or new apps such as potentially projects
    hint: search for `include 'allink_teaser/` 
    
- Added logic to choose which content css classes under the Additional Properties Tab are preselected on creation of content plugin 
    - Create a tuple `INITIAL_CONTENT_CSS_CLASSES` to set which of the `CONTENT_CSS_CLASSES` should be preselected. 
        Add this underneath `CONTENT_CSS_CLASSES`:
        ```
        # Add all content CSS classes here which should be preselected on creation of content plugin
        INITIAL_CONTENT_CSS_CLASSES = (
          'custom-container-width-1',
          'custom-container-width-2',
        )
        ```
      
- changed zip_code field on `AllinkAddressFieldsModel` and deleted ZipCodeField and its form validation
    - if the ZipCodeField has been used on a project you have to manually migrate it.


#### NEW
- Updated README release instructions [#114](https://github.com/allink/allink-core/pull/114)
- Updated mkdoks for new_app command [#115](https://github.com/allink/allink-core/pull/115)
- Updated get chrome translation [#119](https://github.com/allink/allink-core/pull/119)
- Added lazy attribute to iframe embeds [#120](https://github.com/allink/allink-core/pull/120)
- Added alt attribute in any case [#130](https://github.com/allink/allink-core/pull/130)
- Unlinked Brand Logo on browser outdated page [#131](https://github.com/allink/allink-core/pull/131)
- Added logic to choose which content css classes under the Additional Properties Tab are preselected on creation of content plugin [#145](https://github.com/allink/allink-core/pull/145)
- Changed Zip code field on `AllinkAddressFieldsModel` to `Charfield` with `max_length=10` to allow ZipCodes with leading Zeros that are longer than 4 digits [#147](https://github.com/allink/allink-core/pull/147)
    - Deleted ZipCodeField and its form validation
- Added width aliases for list teaser and bg image teaser [#148](https://github.com/allink/allink-core/pull/148)
- Added admin status column and self string representation to new app dummy [#152](https://github.com/allink/allink-core/pull/152)
- Added logo field to allink_categories [#153](https://github.com/allink/allink-core/pull/153)
- Added possibility to override teaser image width alias [#154](https://github.com/allink/allink-core/pull/154)
- Added partner core app [#155](https://github.com/allink/boilerplate-2.0/pull/155)
- Used teaser alt text from original image [#158](https://github.com/allink/allink-core/pull/158)

#### FIXES
- Fixed render_image tag issues with multiple renderings on same site and added unit tests [#116](https://github.com/allink/allink-core/pull/116)
- Fixed autoplay for section videos [#117](https://github.com/allink/allink-core/pull/117)
- Added rel noopener to locations footer template [#121](https://github.com/allink/allink-core/pull/121)
- Changed logic for manual ordering after category so it returns a queryset instead of a list [#127](https://github.com/allink/allink-core/pull/127)
- Added migrations to counter a not null constraint issue in production [#126](https://github.com/allink/allink-core/pull/126)
- Removed migrations from previous PR [#124](https://github.com/allink/allink-core/pull/124) and redid them to consecutive migrations [#128](https://github.com/allink/allink-core/pull/128)
- Fixed teaser links to internal softpages [#129](https://github.com/allink/allink-core/pull/129)
- Removed contact migration [#125](https://github.com/allink/allink-core/pull/125) 
    - if you upgrade an existing project with this the contact migration file will not be deleted
- Hide inactive elements in sitemap [#132](https://github.com/allink/allink-core/pull/132)
- Moved noscript part of tag manager to body [#133](https://github.com/allink/allink-core/pull/133), [#136](https://github.com/allink/allink-core/pull/136)
- Fixed distinct translated items when ordering [#143](https://github.com/allink/allink-core/pull/143)
- Allowed international zip codes [#144](https://github.com/allink/allink-core/pull/144)
- Added logic to display page title as modal header when opened as softpage from teaser instead of button label [#146](https://github.com/allink/allink-core/pull/146)
    
#### DATA MIGRATIONS
- Added custom link option for pagination button on content plugins [~~#118~~(reverted)](https://github.com/allink/allink-core/pull/118) [#124](https://github.com/allink/allink-core/pull/124)
- Added external link to teaser plugin [#123](https://github.com/allink/allink-core/pull/123)
    -  refactored logic so external link is stronger than internal [#139](https://github.com/allink/allink-core/pull/139)
    -  added data-softpage-disabled attribute to link-begin when external link is given [#140](https://github.com/allink/allink-core/pull/140)
    -  added teaser_link_url to teaser admin mixin [#141](https://github.com/allink/allink-core/pull/141)
    -  added teaser_link_url to news item templates [#142](https://github.com/allink/allink-core/pull/142)
    -  added teaser_link_url to teaser_dict property [#142](https://github.com/allink/allink-core/pull/142)
- Added with alias to gallery plugin [#134](https://github.com/allink/allink-core/pull/134)

## v2.7.0
#### IMPORTANT
- Whole area is now clickable on all teasers, added new include/_button.html snippet which is used [#104](https://github.com/allink/allink-core/pull/104)
    - Replace include 'allink_teaser/tile/_link.html' with include 'allink_teaser/includes/_link.html'
    - Adapt teaser styles
- Removed contact button from location footer template [#102](https://github.com/allink/allink-core/pull/102)
    - Use the button plugin to create this button
    - Adapt template in existing projects if its not overridden

#### NEW
- Conditionally output slider content [#98](https://github.com/allink/allink-core/pull/98)
- Wrapped slider plugin to prevent spacings [#100](https://github.com/allink/allink-core/pull/100)
- Updated locations detail template [#106](https://github.com/allink/allink-core/pull/106)
- SEO accordion plugin now has 'Enable SEO FAQ schema' option to add schema.org compliant markup [#108](https://github.com/allink/allink-core/pull/108)
- Updated logic for alt text on images [#110](https://github.com/allink/allink-core/pull/110)

#### FIXES
- Fixed translation for outdated modal [#99](https://github.com/allink/allink-core/pull/99)
- moved Google Tag Manager Code to head [#105](https://github.com/allink/allink-core/pull/105)
- removed skip links from block as they were non-functional [#107](https://github.com/allink/allink-core/pull/107)

## v2.6.3
#### FIXES
- removed Query filter from legacy redirect that removed the last character as it led to multiple matches

## v2.6.2
#### FIXES
- caching of Config model now works as expected and returns correct translated object

## v2.6.1
#### IMPORTANT

#### NEW
- Add list_display fields for news and locations [#93](https://github.com/allink/allink-core/pull/93)
- Update opening hours template [#95](https://github.com/allink/allink-core/pull/95)

#### FIXES
- Remove spaces from link items [#94](https://github.com/allink/allink-core/pull/94)

## v2.6.0
#### IMPORTANT
- Moved browser check logo to container [#67](https://github.com/allink/allink-core/pull/67)
- Adjust browser-suggestion template to be column ready [#88](https://github.com/allink/allink-core/pull/88)
- Fixed locations opening_hours property [#79](https://github.com/allink/allink-core/pull/79)
    - Update location details template if overridden in project

#### NEW
- Used link partial for all links [#66](https://github.com/allink/allink-core/pull/66)
- Grouped content in teaser tile item [#74](https://github.com/allink/allink-core/pull/74)
- Added variable to settings.py to overwrite allowed children of CMSAllinkSEOAccordionPlugin [#76](https://github.com/allink/allink-core/pull/76)
    - Add ```ALLINK_SEOACCORDION_PLUGIN_CHILD_CLASSES = []``` to settings.py
- Used button partial in form base [#81](https://github.com/allink/allink-core/pull/81)
- Removed logo and menu from lockdown page [#82](https://github.com/allink/allink-core/pull/82)
- Disabled image lazyload in menu [#84](https://github.com/allink/allink-core/pull/84)

#### FIXES
- Moved spaceless to link partial [#71](https://github.com/allink/allink-core/pull/71)
- Fixed email translation [#80](https://github.com/allink/allink-core/pull/80)
- Set gallery-plugin autostart to false | set teaser-image ratio default to 16-9 [#87](https://github.com/allink/allink-core/pull/87)

## v2.5.5
#### IMPORTANT
###### TEMPLATES
- if you have overridden base_root.html you need to load google_tag_manager from allink_google_tag_manager_tags instead of google_tag_manager_tags. [#78](https://github.com/allink/allink-core/pull/78)
###### REQUIREMENTS
- we created our own implementation of google_tag_manager so you could remove aldryn_google_tag_manager in the divio control panel. [#78](https://github.com/allink/allink-core/pull/78)
 
## v2.5.4
#### FIXES
- if an image does not exist locally, no exception will be thrown in render_meta_og [#75](https://github.com/allink/allink-core/pull/75)

## v2.5.3
#### FIXES
- Config admin is now translatable [#69](https://github.com/allink/allink-core/pull/69)

## v2.5.2
#### FIXES
- if an image does not exist locally, no exception will be thrown [#68](https://github.com/allink/allink-core/pull/68)

## v2.5.1
#### FIXES
- fix logo link name in browser-check and header
- fix render image tests

## v2.5.0
#### NEW
- Image icon_enabled is now False by default [#55](https://github.com/allink/allink-core/pull/55)
- Added partial for submit buttons [#56](https://github.com/allink/allink-core/pull/56)
- Removed onscreen effect in the allink_content plugin [#57](https://github.com/allink/allink-core/pull/57)
- Added `span` to text link labels [#58](https://github.com/allink/allink-core/pull/58)
- Added logo to browser check template [#60](https://github.com/allink/allink-core/pull/60)

#### FIXES
- Moved styles outside of picture tag (markup validation) [#54](https://github.com/allink/allink-core/pull/54)
- Fixed nested quotes [#59](https://github.com/allink/allink-core/pull/59)

## v2.4.0
#### IMPORTANT
- we removed the app contact from allink_core/apps. you need to delete all occurrences of `allink_apps.contact`, `apps.contact` and `contact-form` [#46](https://github.com/allink/allink-core/pull/46)
- we removed the app event from allink_core/apps. you need to delete all occurrences of `allink_apps.event`, `apps.event` and file `_events.scss` [#48](https://github.com/allink/allink-core/pull/48)
- we removed the app newsletter from allink_core/apps. you need to delete all occurrences of `allink_apps.newsletter`, `apps.newsletter`, `path('mailchimp/'...` in urls.py and file `__signup-form.scss` [#49](https://github.com/allink/allink-core/pull/49)
- we removed the app testimonials from allink_core/apps. you need to delete all occurrences of `allink_apps.testimonials`, `apps.testimonials`, and file `__testimonials.scss` [#51](https://github.com/allink/allink-core/pull/51)
- we removed the app allink_terms from allink_core/core_apps. [#52](https://github.com/allink/allink-core/pull/52)
- we removed the app allink_pdf from allink_core/core_apps. [#52](https://github.com/allink/allink-core/pull/52)
- we removed the app allink_icon from allink_core/core_apps. [#52](https://github.com/allink/allink-core/pull/52) you need to delete `_icon-plugin.scss`.

###### DATA MIGRATIONS
- teaser softpage_enable is now default False [#41](https://github.com/allink/allink-core/pull/41)

#### FIXES
- add proper xmlns:xhtml in sitemap.xml [#40](https://github.com/allink/allink-core/pull/40)
- fixed button link plugin file links [#43](https://github.com/allink/allink-core/pull/43)
- overwrite dragitem.html so AllinkContentColumnPlugin can't be copied or deleted anymore [#45](https://github.com/allink/allink-core/pull/45)
- translate locations opening hours [#52](https://github.com/allink/allink-core/pull/52)

#### NEW
- render_image uses now subject_location by default [#42](https://github.com/allink/allink-core/pull/42)
- AllinkBaseFormPlugin was changed to fit the requirements on current projects [#47](https://github.com/allink/allink-core/pull/47)
- added AllinkBasePluginAjaxCreateView [#47](https://github.com/allink/allink-core/pull/47)

## v2.3.3 
#### FIXES
- Fixed sitemap hreflang with translated parent pages [#34](https://github.com/allink/allink-core/pull/34)
- HrefLangSitemap only returns translated items now [#34](https://github.com/allink/allink-core/pull/34)
- AllinkDetailMixin reverse now defaults to app_label not model_name [#34](https://github.com/allink/allink-core/pull/34)

## v2.3.2
#### IMPORTANT
- Removed `data-softpage` in `link_attributes`. Button Softpage styling now happens via the `icon` parameter.<br>
    When a link should be opened in a softpage use: `data-trigger-softpage`<br>
    For styling use: `data-icon-softpage`<br><br>
    Needs to be changed on project basis. Replace all occurence `data-softpage` with `data-icon-softpage`:
    ```
        // Button Softpage
        &[data-icon-softpage] {
            @include icon-softpage();
        }
    ```
#### NEW
- meta_image is now always a 1200x630px image. (AllinkPageExtension and AllinkSEOFieldsModel) [#33](https://github.com/allink/allink-core/pull/33)
- added field softpage_enabled on teaser plugin [#37](https://github.com/allink/allink-core/pull/37)
- added newsletter/teaser.html template for newsletter-signup-teaser. Data from allink_config wil lbe displayed. (an example for styles can be found in the boilerplate) [#38](https://github.com/allink/allink-core/pull/38)
 
#### FIXES
- AllinkNewsQuerySet latest and earliest now use entry_date not created
- Fixed new-app dummy to import hreflangsitemap
- Fixed mobile order issue in column plugin [#30](https://github.com/allink/allink-core/pull/30)
- Fixed softpage link / header markup errors [#31](https://github.com/allink/allink-core/pull/31)
- Fixed newapp command hreflangsitemap  [#35](https://github.com/allink/allink-core/pull/35)

## v2.3.1
#### IMPORTANT
###### REQUIREMENTS
- removed django-cleanup==2.1.0
- added possibility to add x-y original ratio to width_alias in settings.py [#29](https://github.com/allink/allink-core/pull/29)

## v2.3.0
#### IMPORTANT
- UPDATE REQUIRED: [allink-core-static v2.3.0](https://github.com/allink/allink-core-static/blob/v2.3.0/CHANGELOG.md)
- added 'javascript-catalog' so you need to update our urls.py with
```python
from django.views.i18n import JavaScriptCatalog
...
...i18n_patterns(
...
    path('jsi18n/', JavaScriptCatalog.as_view(domain='django'), name='javascript-catalog'),
...
```

#### NEW
- Added allink_quote plugin
- Added browser-check translations

## v2.2.3
#### IMPORTANT
We added the django_cleanup package
This will delete a file on the filesystem, when a file gets deleted in the django-filer media library.
It does not however delete for example the preview_image on the filesystem if a News entry gets deleted (we also do not delete the filer image/file instance in that case.)
###### REQUIREMENTS
- added django-cleanup==2.1.0
#### NEW
- Added hrefLang to Sitemap [#11](https://github.com/allink/allink-core/pull/11)
    - activate feature for CMS Pages: register `sitemaps = {'cms': CMSHrefLangSitemap}` in project urls.py
    - activate feature for App Detailview: register `class AppName(HrefLangSitemap):` in sitemaps.py in every app
#### FIXES
- fixed fork_app and new_app command [#17](https://github.com/allink/allink-core/pull/17)
- moved language choices from legacylinks models to forms, so no "shadow" migrations will be created on client projects [#12](https://github.com/allink/allink-core/pull/12)
- readded accidentially removed restrictions for news admin lead field

## v2.2.2
#### IMPORTANT
We removed aldryn-common as a dependency as this will no longer be maintained. Replace every occurence of 'aldryn_common' in your project (inlcuding migration files).
Search for: 'aldryn_common.admin_fields.sortedm2m' and replace with 'allink_core.core.models.fields'
###### REQUIREMENTS
- removed aldryn-common (deinstall the divio addon in th control panel)
- added django-sortedm2m==2.0.0
#### NEW
- added sortedm2m model fields to core

## v2.2.1
#### NEW
- refactored customisation commands for new_app and fork_app

## v2.2.0
#### IMPORTANT
- UPDATE REQUIRED: [allink-core-static v2.2.0](https://github.com/allink/allink-core-static/blob/v2.2.0/CHANGELOG.md)
#### NEW
- Video-Plugin:
    - Added autoplay option for mobile devices

## v2.1.0
#### IMPORTANT
- UPDATE REQUIRED: [allink-core-static v2.1.0](https://github.com/allink/allink-core-static/blob/v2.1.0/CHANGELOG.md)

## v2.0.8
#### IMPORTANT
- Required update: [allink-core-static](https://github.com/allink/allink-core-static/commit/1190bda8b5dc38add612be8acb3cb77cfddbc1f6)
#### FIXES
- Cleanup and new elements in styleguide template
- Updated buttons markup in testimonial, app content load more and browser-check templates

## v2.0.7
#### FIXES
- Re-added missing base template markup

## v2.0.6
#### FIXES
- Re-added missing base template markup
- Properly render og tags of app-detail views

## v2.0.5
#### NEW
- refactored buttons: introduced link partial templates, updated other templates accordingly
- added new project setting `BUTTON_CONTEXT_CHOICES`
- removed a lot of template logic from button-link-plugin link template
- removed allink_quote plugin

## v2.0.2
#### NEW
- removed TransactionTestCase and CMSTransactionTestCase where not needed
- removed filter_fields from appcontent plugin
- removed filters param from get_render_queryset_for_display
- moved select manual entries to get_render_queryset_for_display

## v2.0.1
#### NEW
- admin and plugins are no longer translated, we removed every translated string from the admin. This should make translation of the customer specific frontend relevant fields easier.
- The favicon set is now added with an include rather than rendered with a templatetag.
