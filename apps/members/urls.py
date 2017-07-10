# # -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.core.loading import get_class


MembersIndex = get_class('members.views', 'MembersIndex')
MembersProfileEdit = get_class('members.views', 'MembersProfileEdit')


urlpatterns = [
    url(r'^$', MembersIndex.as_view(), name='index'),
    url(r'^profile/edit/$', MembersProfileEdit.as_view(), name='profile_edit'),
]
