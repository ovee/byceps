"""
byceps.services.shop.article.transfer.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import NewType, Optional
from uuid import UUID

from flask_babel import lazy_gettext

from ...shop.transfer.models import ShopID


ArticleID = NewType('ArticleID', UUID)


ArticleNumber = NewType('ArticleNumber', str)


ArticleNumberSequenceID = NewType('ArticleNumberSequenceID', UUID)


@dataclass(frozen=True)
class ArticleNumberSequence:
    id: ArticleNumberSequenceID
    shop_id: ShopID
    prefix: str
    value: int


ArticleType = Enum('ArticleType', ['physical', 'other'])


_ARTICLE_TYPE_LABELS = {
    ArticleType.physical: lazy_gettext('physical'),
    ArticleType.other: lazy_gettext('other'),
}


def get_article_type_label(article_type: ArticleType) -> str:
    """Return a label for the article type."""
    return _ARTICLE_TYPE_LABELS[article_type]


AttachedArticleID = NewType('AttachedArticleID', UUID)


@dataclass(frozen=True)
class Article:
    id: ArticleID
    shop_id: ShopID
    item_number: ArticleNumber
    type_: ArticleType
    description: str
    price: Decimal
    tax_rate: Decimal
    available_from: Optional[datetime]
    available_until: Optional[datetime]
    total_quantity: int
    quantity: int
    max_quantity_per_order: int
    not_directly_orderable: bool
    separate_order_required: bool
    shipping_required: bool
