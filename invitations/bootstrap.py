# -*- coding: utf-8 -*-
"""Setup the invitations application"""
import logging
from invitations import model
from tgext.pluggable import app_model
import transaction

log = logging.getLogger(__name__)


def bootstrap(command, conf, vars):
    log.info('Bootstrapping invitations...')

    model.provider.create(app_model.Permission,
                          {'permission_name': 'invitations-admin',
                           'description': 'Permits to manage invitations'})
    transaction.commit()
    model.DBSession.flush()
