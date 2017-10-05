# -*- coding: utf-8 -*-
import logging
import tg
from tgext.pluggable import PluggableSession

log = logging.getLogger(__name__)

DBSession = PluggableSession()
provider = None

Invite = None


def init_model(app_session):
    DBSession.configure(app_session)


def configure_models():
    global provider, Invite

    if tg.config.get('use_sqlalchemy', False):
        log.info('Configuring Invitations for SQLAlchemy')
        from invitations.model.sqla.models import Invite
        from sprox.sa.provider import SAORMProvider
        provider = SAORMProvider(session=DBSession, engine=False)
    elif tg.config.get('use_ming', False):
        log.info('Configuring Invitations for Ming')
        from invitations.model.ming.models import Invite
        from sprox.mg.provider import MingProvider
        provider = MingProvider(DBSession)
    else:
        raise ValueError('Invitations should be used with sqlalchemy or ming')
