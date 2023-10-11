"""
byceps.services.guest_server.guest_server_domain_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations

from datetime import datetime
import dataclasses

from byceps.events.guest_server import (
    GuestServerApprovedEvent,
    GuestServerCheckedInEvent,
    GuestServerCheckedOutEvent,
    GuestServerRegisteredEvent,
)
from byceps.services.party.models import Party
from byceps.services.user.models.user import User
from byceps.util.result import Err, Ok, Result
from byceps.util.uuid import generate_uuid7

from .errors import (
    AlreadyApprovedError,
    AlreadyCheckedInError,
    AlreadyCheckedOutError,
    NotApprovedError,
    NotCheckedInError,
    PartyIsOverError,
    QuantityLimitReachedError,
    UserUsesNoTicketError,
)
from .models import Address, AddressData, AddressID, Server, ServerID


def ensure_user_may_register_server(
    party: Party,
    user_uses_ticket_for_party: bool,
    user_is_orga_for_party: bool,
    already_registered_server_quantity: int,
) -> Result[
    None, PartyIsOverError | QuantityLimitReachedError | UserUsesNoTicketError
]:
    """Return an error if the user is not allowed to register a(nother)
    guest server for a party.
    """
    if party.is_over:
        return Err(PartyIsOverError())

    if user_is_orga_for_party:
        # Orga needs no ticket and is not bound to quantity limit.
        return Ok(None)

    if not user_uses_ticket_for_party:
        return Err(UserUsesNoTicketError())

    if already_registered_server_quantity >= 5:
        return Err(QuantityLimitReachedError())

    return Ok(None)


def register_server(
    party: Party,
    creator: User,
    owner: User,
    description: str,
    address_datas: set[AddressData],
    *,
    notes_owner: str | None = None,
    notes_admin: str | None = None,
) -> tuple[Server, GuestServerRegisteredEvent]:
    """Register a guest server for a party."""
    server_id = ServerID(generate_uuid7())
    occurred_at = datetime.utcnow()
    addresses = {
        _build_address(server_id, occurred_at, address_data)
        for address_data in address_datas
    }

    server = _build_server(
        server_id,
        party,
        occurred_at,
        creator,
        owner,
        description,
        notes_owner,
        notes_admin,
        addresses,
    )

    event = _build_guest_server_registered_event(server, party, creator, owner)

    return server, event


def _build_address(
    server_id: ServerID, created_at: datetime, address_data: AddressData
) -> Address:
    return Address(
        id=AddressID(generate_uuid7()),
        created_at=created_at,
        server_id=server_id,
        ip_address=address_data.ip_address,
        hostname=address_data.hostname,
        netmask=address_data.netmask,
        gateway=address_data.gateway,
    )


def _build_server(
    server_id: ServerID,
    party: Party,
    created_at: datetime,
    creator: User,
    owner: User,
    description: str,
    notes_owner: str | None,
    notes_admin: str | None,
    addresses: set[Address],
) -> Server:
    return Server(
        id=server_id,
        party_id=party.id,
        created_at=created_at,
        creator=creator,
        owner=owner,
        description=description,
        notes_owner=notes_owner,
        notes_admin=notes_admin,
        approved=False,
        checked_in=False,
        checked_in_at=None,
        checked_out=False,
        checked_out_at=None,
        addresses=addresses,
    )


def _build_guest_server_registered_event(
    server: Server, party: Party, creator: User, owner: User
) -> GuestServerRegisteredEvent:
    return GuestServerRegisteredEvent(
        occurred_at=server.created_at,
        initiator_id=creator.id,
        initiator_screen_name=creator.screen_name,
        party_id=party.id,
        party_title=party.title,
        owner_id=owner.id,
        owner_screen_name=owner.screen_name,
        server_id=server.id,
    )


def approve_server(
    server: Server, initiator: User
) -> Result[tuple[Server, GuestServerApprovedEvent], AlreadyApprovedError]:
    """Approve a guest server."""
    if server.approved:
        return Err(AlreadyApprovedError())

    occurred_at = datetime.utcnow()

    server = dataclasses.replace(server, approved=True)

    event = _build_guest_server_approved_event(server, occurred_at, initiator)

    return Ok((server, event))


def _build_guest_server_approved_event(
    server: Server, occurred_at: datetime, initiator: User
) -> GuestServerApprovedEvent:
    return GuestServerApprovedEvent(
        occurred_at=occurred_at,
        initiator_id=initiator.id,
        initiator_screen_name=initiator.screen_name,
        owner_id=server.owner.id,
        owner_screen_name=server.owner.screen_name,
        server_id=server.id,
    )


def check_in_server(
    server: Server, initiator: User
) -> Result[
    tuple[Server, GuestServerCheckedInEvent],
    AlreadyCheckedInError | AlreadyCheckedOutError | NotApprovedError,
]:
    """Check in a guest server."""
    if not server.approved:
        return Err(NotApprovedError())

    if server.checked_in:
        return Err(AlreadyCheckedInError())

    if server.checked_out:
        return Err(AlreadyCheckedOutError())

    occurred_at = datetime.utcnow()

    server = dataclasses.replace(
        server, checked_in=True, checked_in_at=occurred_at
    )

    event = _build_guest_server_checked_in_event(server, occurred_at, initiator)

    return Ok((server, event))


def _build_guest_server_checked_in_event(
    server: Server, occurred_at: datetime, initiator: User
) -> GuestServerCheckedInEvent:
    return GuestServerCheckedInEvent(
        occurred_at=occurred_at,
        initiator_id=initiator.id,
        initiator_screen_name=initiator.screen_name,
        owner_id=server.owner.id,
        owner_screen_name=server.owner.screen_name,
        server_id=server.id,
    )


def check_out_server(
    server: Server, initiator: User
) -> Result[
    tuple[Server, GuestServerCheckedOutEvent],
    AlreadyCheckedOutError | NotCheckedInError,
]:
    """Check out a guest server."""
    if not server.checked_in:
        return Err(NotCheckedInError())

    if server.checked_out:
        return Err(AlreadyCheckedOutError())

    occurred_at = datetime.utcnow()

    server = dataclasses.replace(
        server, checked_out=True, checked_out_at=occurred_at
    )

    event = _build_guest_server_checked_out_event(
        server, occurred_at, initiator
    )

    return Ok((server, event))


def _build_guest_server_checked_out_event(
    server: Server, occurred_at: datetime, initiator: User
) -> GuestServerCheckedOutEvent:
    return GuestServerCheckedOutEvent(
        occurred_at=occurred_at,
        initiator_id=initiator.id,
        initiator_screen_name=initiator.screen_name,
        owner_id=server.owner.id,
        owner_screen_name=server.owner.screen_name,
        server_id=server.id,
    )
