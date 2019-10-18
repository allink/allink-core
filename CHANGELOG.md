# Changelog
The information for each release is divided into the following chapters:

### IMPORTANT
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
### NEW
new features or plugins
### FIXES
general bugfixes

## v2.2.0
### IMPORTANT
- UPDATE REQUIRED: allink-core-static v2.2.0

## v2.1.0
### IMPORTANT
- UPDATE REQUIRED: allink-core v2.1.0

## v2.0.8
### IMPORTANT
- Required update: [allink-core-static](https://github.com/allink/allink-core-static/commit/1190bda8b5dc38add612be8acb3cb77cfddbc1f6)
### FIXES
- Cleanup and new elements in styleguide template
- Updated buttons markup in testimonial, app content load more and browser-check templates

## v2.0.7
### FIXES
- Re-added missing base template markup

## v2.0.6
### FIXES
- Re-added missing base template markup
- Properly render og tags of app-detail views

## v2.0.5
### NEW
- refactored buttons: introduced link partial templates, updated other templates accordingly
- added new project setting `BUTTON_CONTEXT_CHOICES`
- removed a lot of template logic from button-link-plugin link template
- removed allink_quote plugin

## v2.0.2
### NEW
- removed TransactionTestCase and CMSTransactionTestCase where not needed
- removed filter_fields from appcontent plugin
- removed filters param from get_render_queryset_for_display
- moved select manual entries to get_render_queryset_for_display

## v2.0.1
### NEW
- admin and plugins are no longer translated, we removed every translated string from the admin. This should make translation of the customer specific frontend relevant fields easier.
- The favicon set is now added with an include rather than rendered with a templatetag.