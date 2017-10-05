from tg import url
from tg.decorators import cached_property

import string, random, time, hashlib

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import backref, relation, deferred

from invitations.model import DBSession
from tgext.pluggable import app_model, primary_key
from tgext.pluggable.utils import mount_point

from datetime import datetime, timedelta

DeclarativeBase = declarative_base()

invite_groups_table = Table('invitations_invite_groups', DeclarativeBase.metadata,
                            Column('invite_id', Integer,
                                   ForeignKey('invitations_invite._id',
                                              onupdate="CASCADE",
                                              ondelete="CASCADE"),
                                   primary_key=True),
                            Column('group_id', Integer,
                                   ForeignKey('tg_group.group_id',
                                              onupdate="CASCADE",
                                              ondelete="CASCADE"),
                                   primary_key=True))


class Invite(DeclarativeBase):
    __tablename__ = 'invitations_invite'

    _id = Column(Integer, autoincrement=True, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    user_name = Column(Unicode(255), nullable=False)
    display_name = Column(Unicode(255), nullable=False)
    email_address = Column(Unicode(255), nullable=False)
    code = Column(Unicode(255), nullable=False)
    activated = Column(DateTime)

    user_id = Column(Integer, ForeignKey(primary_key(app_model.User)))
    user = relation(app_model.User, uselist=False,
                    backref=backref('registration', uselist=False, cascade='all'))

    groups = relation(app_model.Group, secondary=invite_groups_table,
                      backref='permissions')

    @classmethod
    def generate_code(cls, email):
        code_space = string.ascii_letters + string.digits

        def _generate_code_impl():
            base = ''.join(random.sample(code_space, 8))
            base += email
            base += str(time.time())
            return hashlib.sha1(base.encode('utf-8')).hexdigest()

        code = _generate_code_impl()
        while DBSession.query(cls).filter_by(code=code).first():
            code = _generate_code_impl()
        return code

    @cached_property
    def activation_link(self):
        return url(mount_point('invitations') + '/activate',
                   params=dict(activation_code=self.code),
                   qualified=True)

    @classmethod
    def clear_expired(cls):
        for expired_reg in DBSession.query(cls).filter_by(activated=None) \
                .filter(cls.time < datetime.now() - timedelta(days=2)):
            DBSession.delete(expired_reg)

    @property
    def dictified(self):
        return vars(self)
