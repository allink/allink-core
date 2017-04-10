# -*- coding: utf-8 -*-

from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save': context.get('show_save', True),
        'hide_save_and_add_another': context.get('hide_save_and_add_another'),
        'hide_save_and_continue': context.get('hide_save_and_continue')
    })

    return ctx
