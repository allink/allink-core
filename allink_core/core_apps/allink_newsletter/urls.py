from django.urls import path

from allink_core.core.loading import get_class

NewsletterSignupView = get_class('allink_newsletter.views', 'NewsletterSignupView')

app_name = 'allink_newsletter'
urlpatterns = [
    path('signup/<int:plugin_id>/', NewsletterSignupView.as_view(), name='signup'),
]
