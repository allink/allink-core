# -*- coding: utf-8 -*-
from allink_core.apps.members.abstract_models import BaseMembers, BaseMembersTranslation, BaseMembersLog
from allink_core.core.loading import is_model_registered

__all__ = []


if not is_model_registered('members', 'Members'):
    class Members(BaseMembers):
        pass

    __all__.append('Members')


if not is_model_registered('members', 'MembersTranslation'):
    class MembersTranslation(BaseMembersTranslation):
        pass

    __all__.append('MembersTranslation')


if not is_model_registered('members', 'MembersLog'):
    class MembersLog(BaseMembersLog):
        pass

    __all__.append('MembersLog')
