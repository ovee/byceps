"""
byceps.services.authentication.password.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from datetime import datetime

from byceps.typing import UserID


@dataclass(frozen=True)
class Credential:
    user_id: UserID
    password_hash: str
    updated_at: datetime