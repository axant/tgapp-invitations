from invitations import model
from tgext.pluggable import app_model


def query_groups():
    _, groups = model.provider.query(app_model.Group)
    primary_field = model.provider.get_primary_field(app_model.Group)
    return [(getattr(group, primary_field), group.display_name) for group in groups]
