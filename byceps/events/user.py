"""
byceps.events.user
~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from dataclasses import dataclass
from typing import Optional

from ..typing import UserID


@dataclass(frozen=True)
class _UserEvent:
    user_id: UserID
    initiator_id: Optional[UserID] = None


@dataclass(frozen=True)
class UserAccountCreated(_UserEvent):
    pass


@dataclass(frozen=True)
class UserAccountDeleted(_UserEvent):
    pass


@dataclass(frozen=True)
class UserAccountSuspended(_UserEvent):
    pass


@dataclass(frozen=True)
class UserAccountUnsuspended(_UserEvent):
    pass


@dataclass(frozen=True)
class UserEmailAddressConfirmed(_UserEvent):
    pass


@dataclass(frozen=True)
class UserScreenNameChanged(_UserEvent):
    old_screen_name: str
    new_screen_name: str
