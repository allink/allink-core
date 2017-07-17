# -*- coding: utf-8 -*-

def create_user(username, email, password, is_staff=False, is_superuser=False,
                base_cms_permissions=False, permissions=None):
    from django.contrib.auth.models import Permission
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        if User.USERNAME_FIELD == 'email':
            user = User.objects.get(**{User.USERNAME_FIELD: email})
        else:
            user = User.objects.get(**{User.USERNAME_FIELD: username})
    except User.DoesNotExist:
        user = User()

    if User.USERNAME_FIELD != 'email':
        setattr(user, User.USERNAME_FIELD, username)

    user.email = email
    user.set_password(password)
    if is_superuser:
        user.is_superuser = True
    if is_superuser or is_staff:
        user.is_staff = True
    user.is_active = True
    user.save()
    if user.is_staff and not is_superuser and base_cms_permissions:
        user.user_permissions.add(Permission.objects.get(codename='add_text'))
        user.user_permissions.add(Permission.objects.get(codename='delete_text'))
        user.user_permissions.add(Permission.objects.get(codename='change_text'))
        user.user_permissions.add(Permission.objects.get(codename='publish_page'))

        user.user_permissions.add(Permission.objects.get(codename='add_page'))
        user.user_permissions.add(Permission.objects.get(codename='change_page'))
        user.user_permissions.add(Permission.objects.get(codename='delete_page'))
    if is_staff and not is_superuser and permissions:
        for permission in permissions:
            user.user_permissions.add(Permission.objects.get(codename=permission))
    return user
