from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from datetime import datetime, timedelta
import time
import hashlib
import random
import string

from invitations.model import DBSession
from tgext.pluggable import app_model

from tg import url
from tg.decorators import cached_property
from tgext.pluggable.utils import mount_point


class Invite(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'invitations_invite'
        indexes = [('activated',), ('email_address',), ('code',),]

    _id = FieldProperty(s.ObjectId)
    time = FieldProperty(s.DateTime, if_missing=datetime.now)
    user_name = FieldProperty(s.String, required=True)
    display_name = FieldProperty(s.String, required=True)
    email_address = FieldProperty(s.String, required=True, index=True)
    code = FieldProperty(s.String)
    activated = FieldProperty(s.DateTime)

    user_id = ForeignIdProperty(app_model.User)

    _groups = ForeignIdProperty(app_model.Group, uselist=True)
    groups = RelationProperty(app_model.Group)

    @classmethod
    def generate_code(cls, email):
        code_space = string.ascii_letters + string.digits

        def _generate_code_impl():
            base = ''.join(random.sample(code_space, 8))
            base += email
            base += str(time.time())
            return hashlib.sha1(base.encode('utf-8')).hexdigest()

        code = _generate_code_impl()
        while cls.query.find({'code': code}).first():
            code = _generate_code_impl()

        return code

    @cached_property
    def activation_link(self):
        return url(mount_point('invitations') + '/activate',
                   params=dict(activation_code=self.code),
                   qualified=True)

    @classmethod
    def clear_expired(cls):
        for expired_reg in cls.query.find(
                {'activated': None, 'time': {'$lte': datetime.now() - timedelta(days=2)}}):
            expired_reg.delete()

    @property
    def dictified(self):
        return dict(
            time=self.time,
            user_name=self.user_name,
            display_name=self.display_name,
            email_address=self.email_address,
            code=self.code,
            activated=self.activated,
            user_id=self.user_id,
            activation_link=self.activation_link,
        )

    @classmethod
    def flush(cls):
        DBSession.flush()
