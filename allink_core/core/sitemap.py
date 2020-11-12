from django.contrib.sitemaps import Sitemap
from django.utils.translation import override as force_language
from cms.sitemaps import CMSSitemap
from allink_core.core.utils import base_url


class CMSHrefLangSitemap(CMSSitemap):
    """
    Base Sitemap class used for djangocms Page objects to provide a proper hreflang tag for each language

    further information: https://support.google.com/webmasters/answer/189077?hl=de

    """

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
