from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
)