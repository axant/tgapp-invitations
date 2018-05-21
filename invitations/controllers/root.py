# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController, config, flash, url, redirect, predicates, request, hooks
from tg.decorators import paginate, expose, validate, require
from tg.i18n import ugettext

from tgext.pluggable import app_model, plug_url,instance_primary_key
from invitations import model
from invitations.lib import get_create_form, send_email


class RootController(TGController):
    allow_only = predicates.has_permission('invitations-invite')

    @expose('invitations.templates.index')
    @paginate('invitations', items_per_page=20)
    def index(self, search_by=None, search_value=None):
        query_args = {'filters': {}}
        if search_by and search_value != '':
            query_args = dict(filters={search_by: search_value},
                              substring_filters=[search_by])
        if not predicates.has_permission('invitations-admin'):
            query_args['filters'].update(
                {'user_who_is_inviting': instance_primary_key(request.identity['user'])}
            )
        _, invitations = model.provider.query(model.Invite, order_by='time', **query_args)
        return dict(invitations=invitations,
                    search_by=search_by,
                    search_value=search_value)

    @expose('invitations.templates.create')
    def create(self, **_):
        return dict(form=get_create_form(),
                    action=plug_url('invitations', '/submit_create'),
                    values=None)

    @expose()
    @validate(get_create_form(), error_handler=create)
    def submit_create(self, **kwargs):
        dictionary = {
            'email_address': kwargs.get('email_address'),
            'message': kwargs.get('message'),
            'user_who_is_inviting': instance_primary_key(request.identity['user']),
            'registration_invite_code':
                model.Invite.generate_registration_invite_code(kwargs.get('email_address')),
        }
        invite = model.provider.create(model.Invite, dictionary)

        invitations_config = config.get('_pluggable_invitations_config')
        mail_body = invitations_config.get(
            'mail_body',
            ugettext('Please click on this link to accept the invite')
            + '\n\n' + kwargs.get('message') + '\n\n' + invite.invite_link,
        )

        email_data = {'sender': config['invitations.email_sender'],
                      'subject': invitations_config.get('mail_subject',
                                                        ugettext('Please accept your invite')),
                      'body': mail_body,
                      'rich': invitations_config.get('mail_rich', '')}

        hooks.notify('invitations.on_submit_create', args=(invite, email_data, kwargs))

        email_data['body'] = email_data['body']
        email_data['rich'] = email_data['rich']

        send_email(kwargs.get('email_address'), **email_data)

        flash(ugettext('Invite created.'))
        return redirect(url(self.mount_point))

    @expose()
    @require(predicates.has_permission('invitations-admin'))
    def delete_invite(self, invite_id):
        primary_field = model.provider.get_primary_field(app_model.Permission)
        model.provider.delete(app_model.Invite, {primary_field: invite_id})

        flash(ugettext('Invite deleted'))
        return redirect(url(self.mount_point))
