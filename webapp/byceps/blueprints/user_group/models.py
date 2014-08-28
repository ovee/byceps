# -*- coding: utf-8 -*-

"""
byceps.blueprints.user_group.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2014 Jochen Kupperschmidt
"""

from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy

from ...database import db, generate_uuid
from ...util.instances import ReprBuilder

from ..user.models import User


class UserGroup(db.Model):
    """A self-organized group of users."""
    __tablename__ = 'user_groups'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    creator_id = db.Column(db.Uuid, db.ForeignKey('users.id'), unique=True)
    creator = db.relationship(User)
    title = db.Column(db.Unicode(40), unique=True)
    description = db.Column(db.Unicode(200))

    members = association_proxy('memberships', 'user')

    def __init__(self, creator, title, description):
        self.creator = creator
        self.title = title
        self.description = description

    @property
    def member_count(self):
        return len(self.members)

    def __repr__(self):
        return ReprBuilder(self) \
            .add_with_lookup('id') \
            .add_with_lookup('title') \
            .add_custom('{:d} members'.format(self.member_count)) \
            .build()


class Membership(db.Model):
    """The assignment of a user to a user group.

    A user must be a member of no more than one group.
    """
    __tablename__ = 'user_group_memberships'

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    group_id = db.Column(db.Uuid, db.ForeignKey('user_groups.id'))
    group = db.relationship(UserGroup, collection_class=set, backref='memberships')
    user_id = db.Column(db.Uuid, db.ForeignKey('users.id'), unique=True)
    user = db.relationship(User, backref='group_membership')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return ReprBuilder(self) \
            .add_with_lookup('id') \
            .add_with_lookup('group') \
            .add_with_lookup('user') \
            .build()
