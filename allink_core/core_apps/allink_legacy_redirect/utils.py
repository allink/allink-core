__all__ = ['strip_anchor_part']


def strip_anchor_part(url):
    return url[:url.index('#')] if '#' in url else url
