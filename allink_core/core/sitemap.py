from django.contrib.sitemaps import Sitemap
from django.utils.translation import override as force_language
from allink_core.apps.config.cms_toolbars import AllinkNoindexExtension, AllinkPageExtension, AllinkTitleExtension
from cms.sitemaps import CMSSitemap

from allink_core.core.utils import base_url
from allink_core.core.loading import get_model

AllinkPageExtension = get_model('config', 'AllinkPageExtension')
AllinkNoindexExtension = get_model('config', 'AllinkNoindexExtension')

class CMSHrefLangSitemap(CMSSitemap):
    """
    Base Sitemap class used for djangocms Page objects to provide a proper hreflang tag for each language

    further information: https://support.google.com/webmasters/answer/189077?hl=de

    """

    def items(self):
        qs = super().items()
        return qs.exclude(
            # because PageExtensions are only available for published pages when the Page was published
            # we need to use the publisher_draft relation to filter for noindex pages
            page__publisher_draft__allinknoindexextension__noindex=True
        ).distinct()

    def _urls(self, page, protocol, domain):
        urls = super()._urls(page, protocol, domain)
        
        for url in urls:
            url['hreflang'] = []
            title = url.get('item')

            for lang in title.page.languages.split(','):
                if title.page.is_published(lang):
                    with force_language(lang):
                        url['hreflang'].append({
                            'lang': lang,
                            'href': '{}{}'.format(base_url(),
                                                  title.page.get_absolute_url(language=lang, fallback=False))
                        })
        return urls


class HrefLangSitemap(Sitemap):
    """
    Base Sitemap class used in allink apps to provide a proper hreflang tag for each language

    further information: https://support.google.com/webmasters/answer/189077?hl=de

    """
    queryset = None  # override in subclass

    def items(self):
        if self.queryset is None:
            raise NotImplementedError("Subclasses of HrefLangSitemap must provide a queryset")
        
        return self.queryset.filter(noindex=False)

    def _urls(self, page, protocol, domain):
        urls = super()._urls(page, protocol, domain)

        for url in urls:
            url['hreflang'] = []
            item = url.get('item')

            for lang in list(item.get_available_languages()):
                url['hreflang'].append({
                    'lang': lang,
                    'href': '{}{}'.format(base_url(), item.get_absolute_url(language=lang))
                })
                url['active'] = item.status

        return urls
