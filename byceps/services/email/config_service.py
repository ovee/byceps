"""
byceps.services.email.config_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2022 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations
from typing import Optional

from sqlalchemy.exc import IntegrityError

from ...database import db, upsert
from ...typing import BrandID

from .dbmodels import EmailConfig as DbEmailConfig
from .transfer.models import EmailConfig, NameAndAddress


class UnknownEmailConfigId(ValueError):
    pass


def create_config(
    brand_id: BrandID,
    sender_address: str,
    *,
    sender_name: Optional[str] = None,
    contact_address: Optional[str] = None,
) -> EmailConfig:
    """Create a configuration."""
    config = DbEmailConfig(
        brand_id,
        sender_address,
        sender_name=sender_name,
        contact_address=contact_address,
    )

    db.session.add(config)
    db.session.commit()

    return _db_entity_to_config(config)


def update_config(
    brand_id: BrandID,
    sender_address: str,
    sender_name: Optional[str],
    contact_address: Optional[str],
) -> EmailConfig:
    """Update a configuration."""
    config = _find_db_config(brand_id)

    if config is None:
        raise UnknownEmailConfigId(
            f'No e-mail config found for brand ID "{brand_id}"'
        )

    config.sender_address = sender_address
    config.sender_name = sender_name
    config.contact_address = contact_address

    db.session.commit()

    return _db_entity_to_config(config)


def delete_config(brand_id: BrandID) -> bool:
    """Delete a configuration.

    It is expected that no database records (sites) refer to the
    configuration anymore.

    Return `True` on success, or `False` if an error occurred.
    """
    get_config(brand_id)  # Verify ID exists.

    try:
        db.session \
            .query(DbEmailConfig) \
            .filter_by(brand_id=brand_id) \
            .delete()

        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False

    return True


def _find_db_config(brand_id: BrandID) -> Optional[DbEmailConfig]:
    return db.session \
        .query(DbEmailConfig) \
        .filter_by(brand_id=brand_id) \
        .one_or_none()


def get_config(brand_id: BrandID) -> EmailConfig:
    """Return the configuration, or raise an error if none is configured
    for that brand.
    """
    config = _find_db_config(brand_id)

    if config is None:
        raise UnknownEmailConfigId(
            f'No e-mail config found for brand ID "{brand_id}"'
        )

    return _db_entity_to_config(config)


def set_config(
    brand_id: BrandID,
    sender_address: str,
    *,
    sender_name: Optional[str] = None,
    contact_address: Optional[str] = None,
) -> None:
    """Add or update configuration for that ID."""
    table = DbEmailConfig.__table__
    identifier = {
        'brand_id': brand_id,
        'sender_address': sender_address,
    }
    replacement = {
        'sender_name': sender_name,
        'contact_address': contact_address,
    }

    upsert(table, identifier, replacement)


def get_all_configs() -> list[EmailConfig]:
    """Return all configurations."""
    configs = db.session.query(DbEmailConfig).all()

    return [_db_entity_to_config(config) for config in configs]


def _db_entity_to_config(config: DbEmailConfig) -> EmailConfig:
    sender = NameAndAddress(
        name=config.sender_name,
        address=config.sender_address,
    )

    return EmailConfig(
        brand_id=config.brand_id,
        sender=sender,
        contact_address=config.contact_address,
    )