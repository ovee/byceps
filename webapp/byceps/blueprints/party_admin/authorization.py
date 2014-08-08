# -*- coding: utf-8 -*-

"""
byceps.blueprints.party_admin.authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2014 Jochen Kupperschmidt
"""

from byceps.util.authorization import create_permission_enum


PartyPermission = create_permission_enum('Party', [
    'list',
])
