from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from datetime import datetime

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
    activated = FieldProperty(s.DateTime)

    email_address = FieldProperty(s.String, required=True)
    message = FieldProperty(s.String, required=True)

    user_who_is_inviting = ForeignIdProperty(app_model.User)
    user_invited = ForeignIdProperty(app_model.User)

    registration_invite_code = FieldProperty(s.String, required=True)
    registration = ForeignIdProperty('Registration')

    @cached_property
    def invite_link(self):
        return url(mount_point('registration'),
                   params=dict(registration_invite_code=self.registration_invite_code),
                   qualified=True)

    @classmethod
    def generate_registration_invite_code(cls, email):
        from hashlib import sha1
        import hmac
        return hmac.new(str(email), str(datetime.now()), sha1).hexdigest()
