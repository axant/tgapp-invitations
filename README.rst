About tgapp-invitations
-------------------------

tgapp-invitations is a Pluggable application for TurboGears2.

allows the users with ``invitations-invite`` permission to invite people via email

this pluggable requires tgapp-registration_ to be plugged

.. _tgapp-registration: https://github.com/axant/tgapp-registration

Installing
-------------------------------

tgapp-invitations can be installed from pypi::

    pip install tgappinvitations

Plugging tgapp-invitations
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with tgappinvitations::

    plug(base_config, 'invitations')

You will be able to access the plugged application at
*http://localhost:8080/invitations*.

Options
-------

- **invite_required** (default: ``True``): when ``False`` the normal tgapp-registration flow is preserved.
