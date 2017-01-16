# # -*- coding: utf-8 -*-
# from django.http import HttpResponse
# from django.utils.module_loading import import_by_path
# from django.views.generic import FormView
#
# from .forms import SignupForm
# from .config import MailChimpConfig
#
#
# config = MailChimpConfig()
#
#
# class SignupView(FormView):
#     form_class = SignupForm
#     template_name = 'allink_mailchimp/plugins/signup_form.html'
#
#     def __init__(self, **kwargs):
#         super(SignupView, self).__init__(**kwargs)
#         if config.signup_form:
#             self.form_class = import_by_path(config.signup_form)
#
#     def post(self, request, *args, **kwargs):
#         print 'inside post'
#
#     def form_valid(self, form):
#         print 'hello from valid'
#         form.save()
#         return HttpResponse('ok')
