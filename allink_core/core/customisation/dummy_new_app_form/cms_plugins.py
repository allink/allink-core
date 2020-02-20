# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseFormPlugin
from .models import DummyAppSignupPlugin
from .forms import DummyAppSignupForm


@plugin_pool.register_plugin
class CMSDummyAppSignupPlugin(CMSAllinkBaseFormPlugin):
    name = 'DummyApp Signup Plugin'
    model = DummyAppSignupPlugin
    render_template = 'dummy_app/plugins/signup/content.html'

    form_class = DummyAppSignupForm
    url_name = 'signup'
