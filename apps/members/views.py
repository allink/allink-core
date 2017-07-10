# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView, FormView
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext_lazy as _

from allauth.account.views import LoginView, AjaxCapableProcessFormViewMixin, PasswordChangeView, PasswordResetView

from allink_core.core.loading import get_class


MembersProfileEditForm = get_class('members.forms', 'MembersProfileEditForm')
send_member_modified_email = get_class('members.email', 'send_member_modified_email')


class MembersIndex(TemplateView):
    template_name = 'members/index.html'


class MembersProfileEdit(FormView):
    form_class = MembersProfileEditForm
    template_name = "members/profile_edit.html"
    success_url = 'members'

    def get_initial(self):
        return {
            'email': self.request.user.email,
        }

    def form_valid(self, form):
        member = self.request.user.members
        member.email = form.cleaned_data.get('email')
        member.save()

        user = self.request.user
        user.email = form.cleaned_data.get('email')
        user.save()

        if 'email' in form.changed_data:
            member.log('email_changed_member', u'Email-Address changed in member-area.')

        if 'first_name' in form.changed_data:
            member.log('first_name_changed_member', u'First name changed in member-area.')

        if 'last_name' in form.changed_data:
            member.log('last_name_name_changed_member', u'Last name changed in member-area.')

        # update mailchimp list
        member.put_to_mailchimp_list(form.initial.get('email'))

        # send notification email to staff
        send_member_modified_email(member)

        return JsonResponse({}, status=200)

    def form_invalid(self, form):
        return JsonResponse({
            'html': render_to_string(
                self.get_template_names(),
                self.get_context_data(form=form),
                request=self.request)
        }, status=400)


class AllinkAccountsAjaxCapableProcessFormViewMixin(AjaxCapableProcessFormViewMixin):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            if form.is_valid():
                response = super(AllinkAccountsAjaxCapableProcessFormViewMixin, self).post(request, *args, **kwargs)
                # handle views with success url
                if self.get_success_url():
                    return JsonResponse({'success_url': self.get_success_url()})

                context = super(AllinkAccountsAjaxCapableProcessFormViewMixin, self).get_context_data()
                try:
                    html = render_to_string(self.confirmation_template, context)
                    return HttpResponse(html)
                # TODO Handel error correctly
                except:
                    # sentry is not configured on localhost
                    if not settings.RAVEN_CONFIG.get('dsn'):
                        raise
                    form.add_error(None, _(u'Something went wrong with your subscription. Please try again later.'))
                    return self.render_to_response(self.get_context_data(form=form), status=206)
            else:
                return self.render_to_response(self.get_context_data(form=form), status=206)
        else:
            return super(AllinkAccountsAjaxCapableProcessFormViewMixin, self).post(request, *args, **kwargs)

    def get_success_url(self):
        success_url = super(AllinkAccountsAjaxCapableProcessFormViewMixin, self).get_success_url()
        from django.core.urlresolvers import reverse, NoReverseMatch
        try:
            return reverse(success_url)
        except NoReverseMatch:
            return success_url


class AllinkLoginView(AllinkAccountsAjaxCapableProcessFormViewMixin, LoginView):
    confirmation_template = 'members/login/confirmation.html'
    success_url = 'members:index'


class AllinkPasswordChangeView(AllinkAccountsAjaxCapableProcessFormViewMixin, PasswordChangeView):
    pass


class AllinkPasswordResetView(AllinkAccountsAjaxCapableProcessFormViewMixin, PasswordResetView):
    pass
