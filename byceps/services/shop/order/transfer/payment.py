"""
byceps.services.shop.order.transfer.payment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2022 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .order import OrderID


AdditionalPaymentData = dict[str, str]


@dataclass(frozen=True)
class Payment:
    id: UUID
    order_id: OrderID
    created_at: datetime
    method: str
    amount: Decimal
    additional_data: AdditionalPaymentData