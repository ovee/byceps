# -*- coding: utf-8 -*-

"""
byceps.services.ticket.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ...blueprints.user.models.user import User
from ...database import db
from ...services.party.models import Party
from ...services.seating.models.category import Category
from ...services.seating.models.seat import Seat

from .models import Ticket


def create_ticket(category, owned_by):
    """Create a single ticket."""
    return create_tickets(category, owned_by, 1)


def create_tickets(category, owned_by, quantity):
    """Create a number of tickets of the same category for a single owner."""
    if quantity < 1:
        raise ValueError('Ticket quantity must be positive.')

    tickets = [Ticket(category, owned_by) for _ in range(quantity)]

    db.session.add_all(tickets)
    db.session.commit()

    return tickets


def find_tickets_related_to_user(user):
    """Return tickets related to the user."""
    return Ticket.query \
        .filter(
            (Ticket.owned_by == user) |
            (Ticket.seat_managed_by == user) |
            (Ticket.user_managed_by == user) |
            (Ticket.used_by == user)
        ) \
        .options(
            db.joinedload('occupied_seat').joinedload('area'),
            db.joinedload('occupied_seat').joinedload('category'),
            db.joinedload('seat_managed_by'),
            db.joinedload('user_managed_by'),
            db.joinedload('used_by'),
        ) \
        .order_by(Ticket.created_at) \
        .all()


def find_tickets_related_to_user_for_party(user, party):
    """Return tickets related to the user for the party."""
    return Ticket.query \
        .for_party_id(party.id) \
        .filter(
            (Ticket.owned_by == user) |
            (Ticket.seat_managed_by == user) |
            (Ticket.user_managed_by == user) |
            (Ticket.used_by == user)
        ) \
        .options(
            db.joinedload('occupied_seat').joinedload('area'),
            db.joinedload('occupied_seat').joinedload('category'),
            db.joinedload('seat_managed_by'),
            db.joinedload('user_managed_by'),
            db.joinedload('used_by'),
        ) \
        .order_by(Ticket.created_at) \
        .all()


def find_tickets_used_by_user(user, party):
    """Return the tickets (if any) used by the user for that party."""
    if user.is_anonymous:
        return []

    return Ticket.query \
        .for_party_id(party.id) \
        .filter(Ticket.used_by == user) \
        .join(Seat) \
        .options(
            db.joinedload('occupied_seat').joinedload('area'),
        ) \
        .order_by(Seat.coord_x, Seat.coord_y) \
        .all()


def uses_any_ticket_for_party(user, party):
    """Return `True` if the user uses any ticket for that party."""
    if user.is_anonymous:
        return False

    count = Ticket.query \
        .for_party_id(party.id) \
        .filter(Ticket.used_by == user) \
        .count()

    return count > 0


def get_attended_parties(user):
    """Return the parties the user has attended."""
    return Party.query \
        .join(Category).join(Ticket).filter(Ticket.used_by == user) \
        .all()


def get_ticket_with_details(ticket_id):
    """Return the ticket with that id, or `None` if not found."""
    return Ticket.query \
        .options(
            db.joinedload('category'),
            db.joinedload('occupied_seat').joinedload('area'),
            db.joinedload('owned_by'),
            db.joinedload('seat_managed_by'),
            db.joinedload('user_managed_by'),
        ) \
        .get(ticket_id)


def get_tickets_with_details_for_party_paginated(party_id, page, per_page):
    """Return the party's tickets to show on the specified page."""
    return Ticket.query \
        .for_party_id(party_id) \
        .options(
            db.joinedload('category'),
            db.joinedload('owned_by'),
            db.joinedload('occupied_seat').joinedload('area'),
        ) \
        .order_by(Ticket.created_at) \
        .paginate(page, per_page)


def get_ticket_count_by_party_id():
    """Return ticket count (including 0) per party, indexed by party ID."""
    return dict(db.session \
        .query(
            Party.id,
            db.func.count(Ticket.id)
        ) \
        .outerjoin(Category) \
        .outerjoin(Ticket) \
        .group_by(Party.id) \
        .all())


def count_tickets_for_party(party):
    """Return the number of "sold" (i.e. generated) tickets for that party."""
    return Ticket.query \
        .for_party_id(party.id) \
        .count()


def get_attendees_by_party(parties):
    """Return the parties' attendees, grouped by party."""
    return {party: get_attendees_for_party(party.id) for party in parties}


def get_attendees_for_party(party_id):
    """Return the party's attendees."""
    return User.query \
        .options(
            db.load_only('screen_name', 'deleted'),
            db.joinedload('avatar_selection').joinedload('avatar')
        ) \
        .join(Ticket.used_by) \
        .join(Category).filter(Category.party_id == party_id) \
        .all()
