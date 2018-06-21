# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template

register = template.Library()


@register.filter('link_attribute_string')
def link_attribute_string(instance, request=None):
    attributes = ''
    attributes += 'target=_blank' if instance.new_window_enabled else ''
    # https://developers.google.com/web/tools/lighthouse/audits/noopener
    attributes += ' rel=noopener' if instance.new_window_enabled else ''
    attributes += ' data-trigger-form-modal' if instance.form_modal_enabled else ''
    attributes += ' data-trigger-image-modal' if instance.image_modal_enabled else ''
    attributes += ' data-trigger-default-modal' if instance.default_modal_enabled else ''
    attributes += ' data-default-modal-variation=video-modal data-default-modal-content-container-id=video-modal-{}'.format(instance.id) if (hasattr(instance, 'template') and getattr(instance, 'template') == 'video_embedded_link') or (hasattr(instance, 'template') and getattr(instance, 'template') == 'video_file_link') else ''

    if instance.image_modal_enabled or instance.default_modal_enabled or instance.form_modal_enabled:
        attributes += ' data-modal-escape-close-method-enabled=true' if hasattr(instance, 'data_modal_escape_close_enabled') and instance.data_modal_escape_close_enabled else ''
        attributes += ' data-modal-overlay-close-method-enabled=true' if hasattr(instance, 'data_modal_overlay_close_enabled') and instance.data_modal_overlay_close_enabled else ''
        attributes += ' data-modal-button-close-method-enabled=true' if hasattr(instance, 'data_modal_button_close_enabled') and instance.data_modal_button_close_enabled else ''

    attributes += ' data-trigger-softpage' if (instance.softpage_large_enabled or instance.softpage_small_enabled) and instance.link_special != 'account_logout' else ''
    attributes += ' data-softpage-variation=large' if instance.softpage_large_enabled else ''
    attributes += ' data-smooth-scroll' if instance.link_anchor else ''
    attributes += ' data-softpage-variation=small' if instance.softpage_small_enabled else ''
    attributes += ' data-softpage-disabled' if instance.link_special == 'account_login' and request.user.is_authenticated else ''
    attributes += ' data-cms-page' if instance.link and (instance.softpage_large_enabled or instance.softpage_small_enabled) else ''
    attributes += ' data-submit-form' if instance.link_special == 'account_logout' and request.user.is_authenticated else ''
    attributes += ' data-form-modal-variation=newsletter-form' if instance.link_special == 'newsletter:signup' else ''
    attributes += ' role=button' if hasattr(instance, "type") and instance.type == 'btn' else ''
    attributes += ' '.join([' {}={}'.format(k, v) if v else ' {}'.format(k) for k, v in instance.link_attributes.items()]) if instance.link_attributes else ''
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
