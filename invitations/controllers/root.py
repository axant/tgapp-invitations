# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController, config, flash, url, redirect, predicates, abort
from tg.decorators import paginate, expose, validate
from tg.i18n import ugettext
from formencode.validators import UnicodeString

from tgext.pluggable import app_model
from invitations import model
from invitations.lib import get_form, get_activate_form, send_email

from datetime import datetime


class RootController(TGController):
    allow_only = predicates.has_permission('invitations-admin')

    @expose('invitations.templates.index')
    @paginate('invitations', items_per_page=20)
    def index(self, search_by=None, search_value=None):
        model.provider.get_entity('Invite').clear_expired()

        query_args = {'filters': {'activated': None}}
        if search_by:
            query_args['filters'].update({search_by: search_value})
            query_args['substring_filters'] = [search_by]
        _, invitations = model.provider.query(model.Invite,
                                              order_by=('email_address',),
                                              **query_args)
        return dict(invitations=invitations,
                    mount_point=self.mount_point)

    @expose()
    def delete_invite(self, invite_id):
        primary_field = model.provider.get_primary_field(app_model.Permission)
        try:
            model.provider.delete(app_model.Invite, {primary_field: invite_id})
        except AttributeError:
            abort(404)
        flash(ugettext('Invite deleted'))
        return redirect(url(self.mount_point))

    @expose('invitations.templates.create')
    def create(self, **kw):
        model.provider.get_entity('Invite').clear_expired()
        return dict(form=get_form(), values=kw, action=self.mount_point + '/submit',
                    mount_point=self.mount_point)

    @expose()
    @validate(get_form(), error_handler=create)
    def submit(self, **kw):
        kw['code'] = model.Invite.generate_code(kw['email_address'])
        invite = model.provider.create(model.Invite, kw)
        return redirect(url(self.mount_point + '/complete'),
                        params=dict(email=invite.email_address))

    @expose('invitations.templates.complete')
    @validate(dict(email=UnicodeString(not_empty=True)), error_handler=index)
    def complete(self, email):
        invite = model.provider.get_obj(model.Invite, {'email_address': email}) or abort(404)
        if not invite:
            return redirect(self.mount_point)

        invite.activation_link  # Force resolution of lazy property

        invitations_config = config.get('_pluggable_invitations_config')
        mail_body = invitations_config.get(
            'mail_body',
            ugettext('Please click on this link to accept the invite'),
        )
        if '%(activation_link)s' not in mail_body:
            mail_body += '\n \n %(activation_link)s'

        email_data = {'sender': config['invitations.email_sender'],
                      'subject': invitations_config.get('mail_subject',
                                                        ugettext('Please accept your invite')),
                      'body': mail_body,
                      'rich': invitations_config.get('mail_rich', '')}

        email_data['body'] = email_data['body'] % invite.dictified
        email_data['rich'] = email_data['rich'] % invite.dictified

        send_email(invite.email_address, **email_data)

        flash(ugettext('Invite created and sent to') + email)
        return redirect(self.mount_point)

    @expose('invitations.templates.activate')
    def activate(self, activation_code, **_):
        invite = model.provider.get_obj(model.Invite,
                                        {'activated': None, 'code': activation_code}) or abort(404)
        invite.activation_code = activation_code
        return dict(form=get_activate_form(),
                    values=invite,
                    action=self.mount_point + '/final_activate',
                    mount_point=self.mount_point)

    @expose('invitations.templates.final_activate')
    @validate(get_activate_form(), error_handler=activate)
    def final_activate(self, **kw):
        invite = model.provider.get_obj(model.Invite,
                                        {'activated': None,
                                         'code': kw.get('activation_code')})  # or abort(404)
        if not invite:
            flash(ugettext('Invite not found or already activated'), 'error')
            return redirect('/')

        u = model.provider.create(app_model.User,
                                  {'user_name': kw.get('user_name'),
                                   'display_name': kw.get('display_name'),
                                   'email_address': invite.email_address,  # it's even disabled
                                   'password': kw.get('password'),
                                   'groups': invite.groups,  # the invited user can't choose them
                                   })

        primary_field = model.provider.get_primary_field(model.Invite)
        model.provider.update(
            model.Invite,
            {primary_field: getattr(invite, primary_field),
             'user_id': str(getattr(u, model.provider.get_primary_field(app_model.User))),
             'activated': datetime.now(),
             'user_name': kw.get('user_name'),
             'display_name': kw.get('display_name'),
             })

        flash(ugettext('Account succesfully activated'))
        return redirect('/')
