from tg.i18n import lazy_ugettext as l_
from tw2.core import Required
from tw2.forms.widgets import Form, TextField, SubmitButton, TextArea
from axf.bootstrap import BootstrapFormLayout
from . import validators
from invitations.lib import helpers as h


class KajikiBootstrapFormLayout(BootstrapFormLayout):
    inline_engine_name = 'kajiki'


class CreateForm(Form):
    class child(KajikiBootstrapFormLayout):
        email_address = TextField(label=l_('Email Address'), css_class='form-control',
                                  validator=validators.UniqueEmailValidator(not_empty=True))
        message = TextArea(label=l_('Message'), css_class='form-control',
                           validator=Required)
    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Invite'))
