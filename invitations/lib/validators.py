from tg.i18n import ugettext as _
from formencode import validators, Invalid
from tgext.pluggable import app_model
from invitations import model
import re


class UniqueEmailValidator(validators.String):
    def validate_python(self, value, state):
        super(UniqueEmailValidator, self)._validate_python(value, state)
        if re.match("^(([A-Za-z0-9]+_+)|([A-Za-z0-9]+\-+)|([A-Za-z0-9]+\.+)|([A-Za-z0-9]+\++))"
                    "*[A-Za-z0-9]+@((\w+\-+)|(\w+\.))*\w{1,63}\.[a-zA-Z]{2,6}$", value):
            count = model.provider.query(app_model.User, filters={'email_address': value})[0]
            count += model.provider.query(model.Invite, filters={'email_address': value})[0]
            if hasattr(app_model, 'Registration'):
                count += model.provider.query(app_model.Registration,
                                              filters={'email_address': value})[0]

            if count != 0:
                raise Invalid(_('Email address has already been taken'), value, state)
        else:
            raise Invalid(_('Invalid email'), value, state)
