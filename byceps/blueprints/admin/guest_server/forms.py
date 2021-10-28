"""
byceps.blueprints.admin.guest_server.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from flask_babel import lazy_gettext
from wtforms import StringField
from wtforms.validators import IPAddress, Optional

from ....util.l10n import LocalizedForm


class SettingUpdateForm(LocalizedForm):
    netmask = StringField(
        lazy_gettext('Netmask'), validators=[Optional(), IPAddress(ipv6=True)]
    )
    gateway = StringField(
        lazy_gettext('Gateway'), validators=[Optional(), IPAddress(ipv6=True)]
    )
    dns_server1 = StringField(
        lazy_gettext('DNS server') + ' 1',
        validators=[Optional(), IPAddress(ipv6=True)],
    )
    dns_server2 = StringField(
        lazy_gettext('DNS server') + ' 2',
        validators=[Optional(), IPAddress(ipv6=True)],
    )
    domain = StringField(lazy_gettext('Domain'), validators=[Optional()])
