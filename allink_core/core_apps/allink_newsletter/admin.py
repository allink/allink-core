from django.contrib import admin

from allink_core.core_apps.allink_newsletter.models import NewsletterSignupLog


@admin.register(NewsletterSignupLog) #Registering the Admin to the corresponding model
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ('salutation', 'first_name', 'last_name', 'email',) #which fields should be shown in the list view