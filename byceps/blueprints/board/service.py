"""
byceps.blueprints.board.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from typing import Dict, Optional, Sequence, Set

from ...services.board.models.posting import Posting as DbPosting
from ...services.ticketing import ticket_service
from ...services.user_badge import service as badge_service
from ...services.user_badge.transfer.models import Badge
from ...typing import BrandID, PartyID, UserID

from .models import Creator


def enrich_creators(postings: Sequence[DbPosting], brand_id: BrandID,
                    party_id: Optional[PartyID]) -> None:
    """Enrich creators with their badges."""
    creator_ids = {posting.creator_id for posting in postings}

    badges_by_user_id = _get_badges(creator_ids, brand_id)

    if party_id is not None:
        ticket_users = ticket_service.select_ticket_users_for_party(
            creator_ids, party_id)
    else:
        ticket_users = set()

    for posting in postings:
        user_id = posting.creator_id

        badges = badges_by_user_id.get(user_id, frozenset())
        uses_ticket = (user_id in ticket_users)

        posting.creator = Creator.from_(posting.creator, badges, uses_ticket)


def _get_badges(user_ids: Set[UserID], brand_id: BrandID
               ) -> Dict[UserID, Set[Badge]]:
    """Fetch users' badges that are either global or belong to the brand."""
    badges_by_user_id = badge_service.get_badges_for_users(user_ids,
                                                           featured_only=True)

    def generate_items():
        for user_id, badges in badges_by_user_id.items():
            selected_badges = {badge for badge in badges
                               if badge.brand_id in {None, brand_id}}
            yield user_id, selected_badges

    return dict(generate_items())
