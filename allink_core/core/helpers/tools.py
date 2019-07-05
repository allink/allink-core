# -*- coding: utf-8 -*-

__all__ = [
    'check_fallback_conf'
]


def check_fallback_conf():
    """
    The get_fallback function fails silently and returns None if no appropriate fallback field is found.
    However it might be interesting to see when the _FIELD_FALLBACK_CONF is not matching the actual attributes on
    the class.

    This helper checks whether all fallback fields are actually on the class which you are trying to implement.
    (e.g. META_FIELD_FALLBACK_CONF, TEASER_FIELD_FALLBACK_CONF)

    :return:
    a list of exceptions which were thrown
    """
    # TODO implementation
    pass
