# -*- coding: utf-8 -*-
"""The tgapp-invitations package"""

import tg
from tg import abort, redirect, url
from tg.configuration import milestones
from tgext.pluggable import instance_primary_key
from tgext.pluggable.utils import mount_point
from datetime import datetime
import json


def plugme(app_config, options):
    from invitations import model
    milestones.config_ready.register(model.configure_models)
    app_config['_pluggable_invitations_config'] = options
    invite_required = options.get('invite_required', True)

    class RegistrationHooks(object):
        @classmethod
        def register(cls, base_config):
            tg.hooks.register('registration.before_registration_form', cls.before_registration_form)
            tg.hooks.register('registration.before_registration', cls.before_registration)
            tg.hooks.register('registration.after_registration', cls.after_registration)
            tg.hooks.register('registration.on_complete', cls.on_complete)
            tg.hooks.register('registration.after_activation', cls.after_activation)

        @staticmethod
        def before_registration_form(kw):
            code = json.loads(kw.get('extra', '{}')).get('registration_invite_code')
            if not code:
                code = kw.get('registration_invite_code')
            invite = model.provider.get_obj(model.Invite, {'registration_invite_code': code})
            if not invite and invite_required:
                abort(412)

            if invite:
                kw['extra'] = json.dumps(
                    dict(registration_invite_code=kw.get('registration_invite_code')))
                kw['email_address'] = invite.email_address
            else:
                kw['extra'] = '{}'

        @staticmethod
        def before_registration(kw):
            extra = json.loads(kw.get('extra'), '{}')
            invite = model.provider.get_obj(
                model.Invite,
                {'registration_invite_code': extra.get('registration_invite_code')},
            )
            if not invite and invite_required:
                abort(412)

        @staticmethod
        def after_registration(reg, kw):
            invite = model.provider.get_obj(
                model.Invite,
                {'registration_invite_code':
                    json.loads(kw['extra']).get('registration_invite_code')})

            if not invite and invite_required:
                abort(412)

            if invite:
                dictionary = model.provider.dictify(invite)
                dictionary.update({'registration': instance_primary_key(reg)})

                model.provider.update(model.Invite, dictionary)

        @staticmethod
        def on_complete(reg, email_data):
            invite = model.provider.get_obj(model.Invite,
                                            {'registration': instance_primary_key(reg)})
            if invite and invite.email_address == reg.email_address:
                # do not send email again as it's already validated
                redirect(url(mount_point('registration') + '/activate',
                         params=dict(code=reg.code),
                         qualified=True))

        @staticmethod
        def after_activation(reg, u):
            invite = model.provider.get_obj(model.Invite,
                                            {'registration': instance_primary_key(reg)})
            if invite:
                dictionary = model.provider.dictify(invite)
                dictionary.update({'user_invited': instance_primary_key(u),
                                   'activated': datetime.now()})
                model.provider.update(model.Invite, dictionary)

    RegistrationHooks.register(app_config)

    return dict(appid='invitations', global_helpers=False)
