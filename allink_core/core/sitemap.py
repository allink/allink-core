from django.conf import settings
from django.contrib.sitemaps import Sitemap
from cms.sitemaps import CMSSitemap
from cms.models.titlemodels import Title


class CMSHrefLangSitemap(CMSSitemap):
    """
    Base Sitemap class used for djangocms Page objects to provide a proper hreflang tag for each language

    further information: https://support.google.com/webmasters/answer/189077?hl=de

    """
    def _urls(self, page, protocol, domain):
        urls = super()._urls(page, protocol, domain)
        for url in urls:
            url['hreflang'] = []
            for lang in settings.LANGUAGES:
                title = url.get('item').page.get_title_obj(language=lang[0], fallback=False)
                if isinstance(title, Title):
                    url['hreflang'].append({
                        'lang': lang[0],
                        'href': "%s://%s/%s/%s/" % (protocol, domain, lang[0], title.slug)
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
                current_item = item.get_translation(lang)
                slug = current_item.slug
                url['hreflang'].append({
                    'lang': lang,
                    'href': "%s://%s/%s/%s/" % (protocol, domain, lang, slug)
                })

        return urls
