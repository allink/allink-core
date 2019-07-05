# -*- coding: utf-8 -*-


def strip_anchor_part(url):
    return url[:url.index('#')] if '#' in url else url
