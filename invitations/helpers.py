# -*- coding: utf-8 -*-

"""WebHelpers used in invitations."""
from invitations import model
from tgext.pluggable.utils import instance_primary_key


def get_primary_field(_model):
    return model.provider.get_primary_field(
        model.provider.get_entity(_model)
    )
