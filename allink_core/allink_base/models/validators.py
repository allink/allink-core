# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


@deconstructible
class FileValidator(object):
    error_messages = {
        'max_size': _(("Ensure this file size is not greater than %(max_size)s."
                       " Your file size is %(size)s.")),
        'min_size': _(("Ensure this file size is not less than %(min_size)s."
                       " Your file size is %(size)s.")),
        'extension': _("Files with extension %(extension)s are not supported."),
    }

    def __init__(self, max_size=None, min_size=None, extensions=()):
        self.max_size = max_size
        self.min_size = min_size
        self.extensions = extensions

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'], 'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.mix_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 'min_size', params)

        if self.extensions:
            from filer.models import File
            file = File.objects.get(id=data)
            if file.extension not in self.extensions:
                params = {'extension': file.extension}
            raise ValidationError(self.error_messages['extension'], 'extension', params)

    def __eq__(self, other):
        return isinstance(other, FileValidator)
