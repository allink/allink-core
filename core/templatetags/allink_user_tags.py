# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template

register = template.Library()


@register.filter('in_one_group')
def in_one_group(user, groups=None):
    """
    Checks if user is at least in one of the provided groups
    """
    return True if any(map(lambda each: each in groups, user.groups.all())) else False
