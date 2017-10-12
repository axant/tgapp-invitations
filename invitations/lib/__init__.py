# -*- coding: utf-8 -*-
from tg import config
from tg import request
from tgext.mailer import Message as message
from tgext.mailer import get_mailer


def send_email(to_addr, sender, subject, body, rich=None):
    mailer = get_mailer(request)
    message_to_send = message(
        subject=subject,
        sender=sender,
        recipients=[to_addr],
        body=body,
        html=rich or None,
    )
    if config.get('tm.enabled', False):
        mailer.send(message_to_send)
    else:
        mailer.send_immediately(message_to_send)


def _get_form(pluggable_id, form_name, form_path):
    _config = config['_pluggable_' + pluggable_id + '_config']
    _form = _config.get(form_name + '_instance')
    if not _form:
        form_path = _config.get(form_name, form_path)
        _module, _form_name = form_path.rsplit('.', 1)
        _module = __import__(_module, fromlist=_form_name)
        _form_class = getattr(_module, _form_name)
        _form = _config[form_name + '_instance'] = _form_class()

    return _form


def get_create_form():
    return _get_form('invitations', 'create_form', 'invitations.lib.forms.CreateForm')
