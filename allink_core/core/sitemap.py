from django.conf import settings
from cms.sitemaps import CMSSitemap
from cms.models.titlemodels import EmptyTitle, Title


class CMSHrefLangSitemap(CMSSitemap):
    def _urls(self, page, protocol, domain):
        import logging
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
                logging.warning(url['hreflang'])

        return urls
