"""
byceps.announce.helpers
~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from typing import Any, Dict, List, Optional

from flask import current_app
import requests

from ..events.base import _BaseEvent
from ..services.webhooks import service as webhook_service
from ..services.webhooks.transfer.models import OutgoingWebhook

from .visibility import get_visibilities


def get_screen_name_or_fallback(screen_name: Optional[str]) -> str:
    """Return the screen name or a fallback value."""
    return screen_name if screen_name else 'Jemand'


def get_webhooks_for_discord(event: _BaseEvent) -> List[OutgoingWebhook]:
    webhook_format = 'discord'
    return webhook_service.get_enabled_outgoing_webhooks(webhook_format)


def get_webhooks_for_irc(event: _BaseEvent) -> List[OutgoingWebhook]:
    webhook_format = 'weitersager'
    webhooks = webhook_service.get_enabled_outgoing_webhooks(webhook_format)

    visibilities = get_visibilities(event)
    if not visibilities:
        current_app.logger.warning(
            f'No visibility assigned for event type "{type(event)}".'
        )
        return []

    def match(webhook):
        return any(
            match_scope(webhook, visibility.name, None)
            for visibility in visibilities
        )

    webhooks = [wh for wh in webhooks if match(wh)]

    if not webhooks:
        current_app.logger.warning(
            f'No enabled IRC webhooks found. Not sending message to IRC.'
        )
        return []

    # Stable order is easier to test.
    webhooks.sort(key=lambda wh: wh.extra_fields['channel'])

    return webhooks


def match_scope(webhook: OutgoingWebhook, scope: str, scope_id: str) -> bool:
    return webhook.scope == scope and webhook.scope_id == scope_id


def call_webhook(webhook: OutgoingWebhook, text: str) -> None:
    """Send HTTP request to the webhook."""
    text_prefix = webhook.text_prefix
    if text_prefix:
        text = text_prefix + text

    data = _assemble_request_data(webhook, text)

    requests.post(webhook.url, json=data)  # Ignore response code for now.


def _assemble_request_data(
    webhook: OutgoingWebhook, text: str
) -> Dict[str, Any]:
    if webhook.format == 'discord':
        return {'content': text}

    elif webhook.format == 'weitersager':
        channel = webhook.extra_fields.get('channel')
        if not channel:
            current_app.logger.warning(
                f'No channel specified with IRC webhook.'
            )

        return {'channel': channel, 'text': text}
