# https://github.com/divio/aldryn-newsblog/blob/9d2730b932b23ee7ef768e2b32c847b3472ceb34/aldryn_newsblog/tests/test_views.py
PARLER_LANGUAGES_HIDE = {
    1: [
        {
            'code': u'en',
            'fallbacks': [u'de'],
            'hide_untranslated': True
        },
        {
            'code': u'de',
            'fallbacks': [u'en'],
            'hide_untranslated': True
        },
        {
            'code': u'fr',
            'fallbacks': [u'en'],
            'hide_untranslated': True
        },
    ],
    'default': {
        'hide_untranslated': True,
        'fallbacks': [],
    }
}

PARLER_LANGUAGES_SHOW = {
    1: [
        {
            'code': u'en',
            'fallbacks': [u'de'],
            'hide_untranslated': False
        },
        {
            'code': u'de',
            'fallbacks': [u'en'],
            'hide_untranslated': False
        },
        {
            'code': u'fr',
            'fallbacks': [u'en'],
            'hide_untranslated': False
        },
    ],
    'default': {
        'hide_untranslated': False,
        'fallbacks': [],
    }
}
