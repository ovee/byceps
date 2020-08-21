"""
byceps.announce.irc.user_badge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Announce user badge events on IRC.

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ...events.user_badge import UserBadgeAwarded
from ...services.user import service as user_service
from ...signals import user_badge as user_badge_signals
from ...typing import UserID
from ...util.irc import send_message
from ...util.jobqueue import enqueue

from ..helpers import get_screen_name_or_fallback

from ._config import CHANNEL_ORGA_LOG


@user_badge_signals.user_badge_awarded.connect
def _on_user_badge_awarded(sender, *, event: UserBadgeAwarded) -> None:
    enqueue(announce_user_badge_awarded, event)


def announce_user_badge_awarded(event: UserBadgeAwarded) -> None:
    """Announce that a badge has been awarded to a user."""
    channels = [CHANNEL_ORGA_LOG]

    initiator_screen_name = _get_screen_name(event.initiator_id)
    awardee_screen_name = get_screen_name_or_fallback(event.user_screen_name)

    text = (
        f'{initiator_screen_name} hat das Abzeichen "{event.badge_label}" '
        f'an {awardee_screen_name} verliehen.'
    )

    send_message(channels, text)


def _get_screen_name(user_id: UserID) -> str:
    screen_name = user_service.find_screen_name(user_id)
    return get_screen_name_or_fallback(screen_name)
