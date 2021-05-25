"""
byceps.application.blueprints.blueprints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from typing import Iterator, Optional, Tuple

from flask import Flask

from .. import config
from ..util.framework.blueprint import register_blueprint


BlueprintReg = Tuple[str, Optional[str]]


def register_blueprints(app: Flask) -> None:
    """Register blueprints depending on the configuration."""
    for parent, name, url_prefix in _get_blueprints(app):
        register_blueprint(parent, name, url_prefix)


def _get_blueprints(app: Flask) -> Iterator[BlueprintReg]:
    """Yield blueprints to register on the application."""
    yield from _get_blueprints_common(app)

    current_mode = config.get_app_mode(app)
    if current_mode.is_site():
        yield from _get_blueprints_site(app)
    elif current_mode.is_admin():
        yield from _get_blueprints_admin(app)

    yield from _get_blueprints_api(app)

    yield from _get_blueprints_monitoring(app)

    if app.debug:
        yield from _get_blueprints_debug(app)


def _get_blueprints_common(app: Flask) -> Iterator[BlueprintReg]:
    yield from [
        (app, 'common.authentication.password',  '/authentication/password' ),
        (app, 'common.core',                     '/core'                    ),
        (app, 'common.locale',                   '/locale'                  ),
    ]


def _get_blueprints_site(app: Flask) -> Iterator[BlueprintReg]:
    yield from [
        (app, 'site.attendance',                 '/attendance'              ),
        (app, 'site.authentication.login',       '/authentication'          ),
        (app, 'site.board',                      '/board'                   ),
        (app, 'site.consent',                    '/consent'                 ),
        (app, 'site.dashboard',                  '/dashboard'               ),
        (app, 'site.news',                       '/news'                    ),
        (app, 'site.newsletter',                 '/newsletter'              ),
        (app, 'site.orga_team',                  '/orgas'                   ),
        (app, 'site.party',                      None                       ),
        (app, 'site.seating',                    '/seating'                 ),
        (app, 'site.shop.order',                 '/shop'                    ),
        (app, 'site.shop.orders',                '/shop/orders'             ),
        (app, 'site.snippet',                    None                       ),
        (app, 'site.terms',                      '/terms'                   ),
        (app, 'site.ticketing',                  '/tickets'                 ),
        (app, 'site.tourney',                    '/tourneys'                ),
        (app, 'site.user.avatar',                '/users'                   ),
        (app, 'site.user.creation',              '/users'                   ),
        (app, 'site.user.current',               '/users'                   ),
        (app, 'site.user.settings',              '/users/me/settings'       ),
        (app, 'site.user.email_address',         '/users/email_address'     ),
        (app, 'site.user_profile',               '/users'                   ),
        (app, 'site.user_badge',                 '/user_badges'             ),
        (app, 'site.user_group',                 '/user_groups'             ),
        (app, 'site.user_message',               '/user_messages'           ),
    ]


def _get_blueprints_admin(app: Flask) -> Iterator[BlueprintReg]:
    yield from [
        (app, 'admin.attendance',                '/admin/attendance'        ),
        (app, 'admin.authentication.login',      '/authentication'          ),
        (app, 'admin.authorization',             '/admin/authorization'     ),
        (app, 'admin.board',                     '/admin/boards'            ),
        (app, 'admin.brand',                     '/admin/brands'            ),
        (app, 'admin.consent',                   '/admin/consent'           ),
        (app, 'admin.core',                      None                       ),
        (app, 'admin.dashboard',                 '/admin/dashboard'         ),
        (app, 'admin.news',                      '/admin/news'              ),
        (app, 'admin.newsletter',                '/admin/newsletter'        ),
        (app, 'admin.jobs',                      '/admin/jobs'              ),
        (app, 'admin.maintenance',               '/admin/maintenance'       ),
        (app, 'admin.more',                      '/admin/more'              ),
        (app, 'admin.orga',                      '/admin/orgas'             ),
        (app, 'admin.orga_presence',             '/admin/presence'          ),
        (app, 'admin.orga_team',                 '/admin/orga_teams'        ),
        (app, 'admin.party',                     '/admin/parties'           ),
        (app, 'admin.seating',                   '/admin/seating'           ),
        (app, 'admin.shop',                      None                       ),
        (app, 'admin.shop.article',              '/admin/shop/articles'     ),
        (app, 'admin.shop.email',                '/admin/shop/email'        ),
        (app, 'admin.shop.order',                '/admin/shop/orders'       ),
        (app, 'admin.shop.shipping',             '/admin/shop/shipping'     ),
        (app, 'admin.shop.shop',                 '/admin/shop/shop'         ),
        (app, 'admin.shop.storefront',           '/admin/shop/storefronts'  ),
        (app, 'admin.site',                      '/admin/sites'             ),
        (app, 'admin.snippet',                   '/admin/snippets'          ),
        (app, 'admin.terms',                     '/admin/terms'             ),
        (app, 'admin.ticketing',                 '/admin/ticketing'         ),
        (app, 'admin.ticketing.category',        '/admin/ticketing/categories'  ),
        (app, 'admin.ticketing.checkin',         '/admin/ticketing/checkin' ),
        (app, 'admin.tourney',                   None                       ),
        (app, 'admin.tourney.category',          '/admin/tourney/categories'),
        (app, 'admin.tourney.tourney',           '/admin/tourney/tourneys'  ),
        (app, 'admin.user',                      '/admin/users'             ),
        (app, 'admin.user_badge',                '/admin/user_badges'       ),
        (app, 'admin.webhook',                   '/admin/webhooks'          ),
    ]


def _get_blueprints_api(app: Flask) -> Iterator[BlueprintReg]:
    yield from [
        (app, 'api.v1.attendance',               '/api/v1/attendances'      ),
        (app, 'api.v1.snippet',                  '/api/v1/snippets'         ),
        (app, 'api.v1.tourney.avatar',           '/api/v1/tourney/avatars'  ),
        (app, 'api.v1.tourney.match.comments',   '/api/v1/tourney'          ),
        (app, 'api.v1.user',                     '/api/v1/users'            ),
        (app, 'api.v1.user_avatar',              '/api/v1/user_avatars'     ),
        (app, 'api.v1.user_badge',               '/api/v1/user_badges'      ),
    ]


def _get_blueprints_monitoring(app: Flask) -> Iterator[BlueprintReg]:
    yield from [
        (app, 'monitoring.healthcheck',      '/health'                  ),
    ]

    if app.config['METRICS_ENABLED']:
        yield from [
            (app, 'monitoring.metrics',          '/metrics'                 ),
        ]


def _get_blueprints_debug(app: Flask) -> Iterator[BlueprintReg]:
    yield from [
        (app, 'common.style_guide',              '/style_guide'             ),
    ]
