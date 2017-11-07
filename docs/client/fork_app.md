# Forking an app

The following guide explains how you can override an app from allink-core/apps.

We provided you with a management command <code>fork_app</code>.

The Following command will create a new module called <code>work</code> inside the directory <code>allink_apps/</code>
```
./manage.py fork_app work allink_apps
```


!!! note
    It would be possible to fork an app in every directory you want. However to keep a certain structure in all our projects we always create a directory <code>allink_apps</code>.


The console will output the steps needed to complete the process.
```
The final step is uncomment "new_app.config" in OVERIDDED_ALLINK_CORE_APPS (replacing
the equivalent allink_core app). e.g.:

    # settings.py
    ...

    OVERIDDEN_ALLINK_CORE_APPS = [
        # 'allink_apps.contact',
        # 'allink_apps.events',
        # 'allink_apps.locations',
        # 'allink_apps.news',
        # 'allink_apps.members',
        # 'allink_apps.people',
        # 'allink_apps.testimonials',
        # 'allink_apps.work',
    ]
```

The files which have been created just provide you with the minimal file structure. But you are now ready to override and extend what ever you want.


For a some more guidance use the management command <code>fork_app_help</code>. This provides you with some usefull comments in every file.
```
./manage.py fork_app_help work allink_apps
```