# AllinkMandrillEmailBase
basic implementation. "from" and "to" addresses will be used like specified in AllinkConfig as fallback the addresses in the settings.py will be used: ALLINK_MANDRILL_DEV_MODE_FROM_EMAIL_ADDRESS, ALLINK_MANDRILL_DEV_MODE_TO_EMAIL_ADDRESSES.
```python
from django.utils.translation import ugettext_lazy as _
from apps.jobs.email_mandrill import AllinkMandrillEmailBase


class InternalSupportMail(AllinkMandrillEmailBase):
    template_name = 'projectname_formname_internal'

    def build_subject(self):
        return _('My Subject')

    def fetch_to_email_addresses(self):
        return [
            self.create_email_to_entry('itcrowd@allink.ch', 'Hans Mustermann'),
        ]

    def build_body(self):
        return [
            self.create_global_merge_var('title', 'My Title',),
        ]




# Basic usage:
InternalSupportMail(language=get_language()).send_mail()

```
Override from, to and reply to addresses
```python
from django.utils.translation import ugettext_lazy as _
from apps.jobs.email_mandrill import AllinkMandrillFormEmail


class InternalSupportMail(AllinkMandrillEmailBase):
    ...
    def get_from_mail_address(self):
        return 'sender@allink.ch'

    def fetch_to_email_addresses(self):
        return [
            self.create_email_to_entry('itcrowd@allink.ch', 'Hans Mustermann'),
        ]

    def get_from_name(self):
        return 'Peter Pattern'

```
write logs, when email is sent. You have to implement the appropriate log tabel and functionality by yourself. "create_log_entry()"
```python
from django.utils.translation import ugettext_lazy as _
from apps.jobs.email_mandrill import AllinkMandrillFormEmail


class InternalAdditionalSupportMail(AllinkMandrillEmailBase):
    def __init__(self, template_name='%%%', logging=True):
        super().__init__(*args, **kwargs)


    def build_body(self):
        complicated_text = get_complicated_might_contain_linebreaks()

        return [
            self.create_global_merge_var(
                'title',
                self.replace_linebreaks_with_html(complicated_text),
            ),
        ]

    def log(self, **kwargs):
        mail_sent_summary = _('Subject: {} || sent to: {}').format(kwargs['subject'],
                                                                   ''.join(
                                                                       element['email'] + ' ' for element in
                                                                       kwargs['to']))
        create_log_entry(mail_sent_summary)
```
# AllinkMandrillFormEmail
basic implementation
```python
from django.utils.translation import ugettext_lazy as _
from apps.jobs.email_mandrill import AllinkMandrillFormEmail


class InternalSupportMail(AllinkMandrillFormEmail):
    template_name = 'projectname_formname_internal'

    def build_subject(self):
        return _('My Subject')

    # only if you want to add additional merge vars, the form fields are already added
    def build_body(self):
        body = super.build_body()
        return body.extend([
            self.create_global_merge_var('title', 'My Title',),
        ])


# Basic usage:
InternalSupportMail(form=someform, language=get_language()).send_mail()
```
