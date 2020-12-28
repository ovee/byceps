"""
byceps.services.webhooks.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from typing import Any, Dict, Optional

from sqlalchemy.ext.mutable import MutableDict

from ...database import db, generate_uuid


class OutgoingWebhook(db.Model):
    """An outgoing webhook configuration."""

    __tablename__ = 'outgoing_webhooks'
    __table_args__ = (
        db.UniqueConstraint('scope', 'scope_id'),
    )

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    scope = db.Column(db.UnicodeText, nullable=False)
    scope_id = db.Column(db.UnicodeText, nullable=True)
    format = db.Column(db.UnicodeText, nullable=False)
    text_prefix = db.Column(db.UnicodeText, nullable=True)
    extra_fields = db.Column(MutableDict.as_mutable(db.JSONB), nullable=True)
    url = db.Column(db.UnicodeText, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    def __init__(
        self,
        scope: str,
        scope_id: Optional[str],
        format: str,
        url: str,
        enabled: bool,
        *,
        text_prefix: Optional[str] = None,
        extra_fields: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.scope = scope
        self.scope_id = scope_id
        self.format = format
        self.text_prefix = text_prefix
        self.extra_fields = extra_fields
        self.url = url
        self.enabled = enabled
