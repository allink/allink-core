# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template

register = template.Library()


@register.filter('link_attribute_string')
def link_attribute_string(instance, request=None):
    attributes = ''
    attributes += 'target="_blank"' if instance.new_window_enabled else ''
    attributes += ' data-trigger-form-modal' if instance.image_modal_enabled else ''
    attributes += ' data-trigger-image-modal' if instance.image_modal_enabled else ''
    attributes += ' data-cms-page' if instance.is_page_link else ''
    attributes += ' data-trigger-softpage' if (instance.softpage_large_enabled or instance.softpage_small_enabled) and instance.link_special != 'account_logout' else ''
    attributes += ' data-softpage-variation="large"' if instance.softpage_large_enabled else ''
    attributes += ' data-smooth-scroll' if instance.link_anchor else ''
    attributes += ' data-softpage-variation="small"' if instance.softpage_small_enabled else ''
    attributes += ' data-softpage-disabled' if instance.link_special == 'account_login' and request.user.is_authenticated else ''
    attributes += ' data-submit-form' if instance.link_special == 'account_logout' and request.user.is_authenticated else ''
    attributes += ' role="button"' if hasattr(instance, "type") and instance.type == 'btn' else ''
    return attributes


@register.filter('link_classes')
def link_classes(instance):
    classes = ''
    if hasattr(instance, 'type'):
        if instance.type == 'btn':
            classes += ' btn'
            if instance.btn_context:
                classes += ' btn-{}'.format(instance.btn_context)
            if instance.btn_size:
                classes += ' btn-{}'.format(instance.btn_size)
            if instance.btn_block:
                classes += ' btn-{}'.format(instance.btn_block)
        else:
            classes += ' text'
    return classes
