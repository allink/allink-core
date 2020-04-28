# Create a new app

This guide describes the fastest way to how you can create an app which inherits from <code>allink_core.core.models.models.AllinkBaseModel</code>. The main reason you want to do that is that the new app automatically fits in the allink ecosystem. The created module will provide you with all the default plugins, forms and views (like a standard 'allink app').

The management command <code>new_app</code> will create a new app in the specified directory.
```
./manage.py new_app my_new_app apps
```
The console output will guide you with the steps needed to get your new app up and running.
```
The final steps:
1. add 'apps.my_new_app' to PROJECT_APPS
2. add Plugins to CMS_ALLINK_CONTENT_PLUGIN_CHILD_CLASSES
3. define templates/ create a new tuple MYNEWAPP_PLUGIN_TEMPLATES
4. (optional) add '('mynewapp', 'MyNewApp'),' to PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES if the app should have categories
5. create all required templates (default grid_static and search, detail and no_result)
6. ./manage.py makemigrations my_new_app ./manage.py migrate
```