"""
:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from decimal import Decimal

from pytest import raises

from byceps.database import generate_uuid
from byceps.services.shop.article.transfer.models import (
    Article,
    ArticleID,
    ArticleNumber,
    ArticleType,
)
from byceps.services.shop.cart.models import CartItem
from byceps.services.shop.shop.transfer.models import ShopID


def test_init_with_positive_quantity():
    quantity = 1

    item = create_item(quantity)

    assert item.quantity == quantity


def test_init_with_zero_quantity():
    with raises(ValueError):
        create_item(0)


def test_init_with_negative_quantity():
    with raises(ValueError):
        create_item(-1)


# helpers


def create_item(quantity: int) -> CartItem:
    article = create_article()
    return CartItem(article, quantity)


def create_article() -> Article:
    return Article(
        id=ArticleID(generate_uuid()),
        shop_id=ShopID('any-shop'),
        item_number=ArticleNumber('article-123'),
        type_=ArticleType.other,
        description='Cool thing',
        price=Decimal('1.99'),
        tax_rate=Decimal('0.19'),
        available_from=None,
        available_until=None,
        total_quantity=1,
        quantity=1,
        max_quantity_per_order=1,
        not_directly_orderable=False,
        separate_order_required=False,
        shipping_required=False,
    )
