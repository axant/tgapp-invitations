About tgapp-invitations
-------------------------

tgapp-invitations is a Pluggable application for TurboGears2.

Installing
-------------------------------

tgapp-invitations can be installed both from pypi or from bitbucket::

    pip install tgappinvitations

should just work for most of the users

Plugging tgapp-invitations
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with tgappinvitations::

    plug(base_config, 'tgappinvitations')

You will be able to access the plugged application at
*http://localhost:8080/tgappinvitations*.

Available Hooks
----------------------

tgapp-invitations makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

Exposed Partials
----------------------

tgapp-invitations exposes a bunch of partials which can be used
to render pieces of the blogging system anywhere in your
application:

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

