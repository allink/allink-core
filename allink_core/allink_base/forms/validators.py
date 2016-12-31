# -*- coding: utf-8 -*-


def validate_file_extension(value, valid_extensions):
    """
    :param value:
        - field value
    :param valid_extensions:
        - list of valid fileextensions e.g ['.pdf', '.docx']
    :return:
    """
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')
