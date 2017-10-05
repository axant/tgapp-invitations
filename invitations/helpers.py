# -*- coding: utf-8 -*-

"""WebHelpers used in invitations."""
from tgext.pluggable import app_model
from invitations import model
import six


def get_primary_field(_model):
    return model.provider.get_primary_field(
        model.provider.get_entity(_model)
    )
