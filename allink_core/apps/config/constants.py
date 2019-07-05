PAGE_META_FIELD_FALLBACK_CONF = {
    'meta_image': [
        {'model': 'self', 'field': 'allinkpageextension.og_image', },
        {'model': 'self', 'field': 'allinkpageextension.teaser_image', },
        {'model': 'config.Config', 'field': 'default_og_image', },
    ],
    'meta_title': [
        {'model': 'cms.Title', 'field': 'allinktitleextension.og_title', },
        {'model': 'cms.Title', 'field': 'allinktitleextension.teaser_title', },
        {'model': 'self', 'field': 'get_page_title', },
    ],
    'meta_description': [
        {'model': 'cms.Title', 'field': 'allinktitleextension.og_description', },
        {'model': 'cms.Title', 'field': 'allinktitleextension.teaser_description', },
    ],
}

PAGE_TEASER_FIELD_FALLBACK_CONF = {
    'teaser_image': [
        {'model': 'self', 'field': 'allinkpageextension.teaser_image', },
    ],
    'teaser_title': [
        {'model': 'cms.Title', 'field': 'allinktitleextension.teaser_title', },
        {'model': 'self', 'field': 'get_page_title', },
    ],
    'teaser_technical_title': [
        {'model': 'cms.Title', 'field': 'allinktitleextension.teaser_technical_title', },
    ],
    'teaser_description': [
        {'model': 'cms.Title', 'field': 'allinktitleextension.teaser_description', },
    ],
    'teaser_link_text': [
        {'model': 'cms.Title', 'field': 'allinktitleextension.teaser_link_text', },
        {'model': 'settings', 'field': 'TEASER_PAGE_LINK_TEXT', },
    ],
}

PAGE_FIELD_FALLBACK_CONF = {**PAGE_META_FIELD_FALLBACK_CONF, **PAGE_TEASER_FIELD_FALLBACK_CONF}
