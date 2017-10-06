from formencode.validators import UnicodeString, FieldsMatch
from tg.i18n import lazy_ugettext as l_
from tw2.core import Deferred, Required
from tw2.forms.widgets import Form, TextField, SubmitButton, MultipleSelectField, PasswordField,\
                              HiddenField
from axf.bootstrap import BootstrapFormLayout
from . import validators
from invitations.lib import helpers as h


class KajikiBootstrapFormLayout(BootstrapFormLayout):
    inline_engine_name = 'kajiki'


class InviteForm(Form):
    class child(KajikiBootstrapFormLayout):
        activation_code = HiddenField()
        user_name = TextField(label=l_('User Name'), css_class='form-control',
                              validator=UnicodeString(min=3, max=255))
        display_name = TextField(label=l_('Display Name'), css_class='form-control',
                                 validator=UnicodeString(min=3, max=255))
        email_address = TextField(label=l_('Email Address'), css_class='form-control',
                                  validator=validators.UniqueEmailValidator(not_empty=True))
        groups = MultipleSelectField(label=l_('Permission Groups'), css_class="form-control",
                                     options=Deferred(h.query_groups))
    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Invite'))


class ActivateForm(Form):
    class child(KajikiBootstrapFormLayout):
        activation_code = HiddenField()
        password = PasswordField(label=l_('Password'), css_class='form-control',
                                 validator=Required)
        password_confirm = PasswordField(label=l_('Confirm Password'), css_class='form-control',
                                         validator=Required)
        validator = FieldsMatch('password', 'password_confirm')
        user_name = TextField(label=l_('User Name'), css_class='form-control',
                              validator=UnicodeString(min=3, max=255))
        display_name = TextField(label=l_('Display Name'), css_class='form-control',
                                 validator=UnicodeString(min=3, max=255))
    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Save'))
