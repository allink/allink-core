from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.views.i18n import JavaScriptCatalog
from allink_core.core.sitemap import CMSHrefLangSitemap
from allink_core.apps.news.sitemaps import NewsSitemap

sitemaps = {
    'cms': CMSHrefLangSitemap,
    'news': NewsSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps}),
    path('styleguide/', include('allink_core.core_apps.allink_styleguide.urls', namespace='styleguide')),
    path('cms-api/', include('allink_core.core_apps.allink_cms.urls', namespace='cms_api')),

] + i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(domain='django'), name='javascript-catalog'),
    path('sitemap.xml', sitemap_view, {'sitemaps': sitemaps}),
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
)
