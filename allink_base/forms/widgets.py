# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class AdminPdfThumnailWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []

        if value:
            output.append(u'<img alt="%s" src="%s" height="200"/>' % (value.url, value.url,))
        else:
            output.append(_(u'Thumbnail is created when publication is saved. And a PDF document is assigned.'))

        # This is commented out b/c maybe you want to be able to override the thumbnail?
        # output.append(super(AdminFileWidget, self).render(name, value, attrs))

        return mark_safe(u''.join(output))
