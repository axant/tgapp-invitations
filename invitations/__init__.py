# -*- coding: utf-8 -*-
"""The tgapp-invitations package"""

from tg.configuration import milestones


def plugme(app_config, options):
    from invitations import model
    milestones.config_ready.register(model.configure_models)
    app_config['_pluggable_invitations_config'] = options

    return dict(appid='invitations', global_helpers=False)
