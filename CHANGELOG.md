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

## v2.5.0
###### NEW
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
