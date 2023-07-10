"""
byceps.config
~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from flask import current_app, Flask


EXTENSION_KEY = 'byceps_config'


class AppMode(Enum):
    admin = object()
    base = object()
    cli = object()
    site = object()
    worker = object()

    def is_admin(self) -> bool:
        return self == AppMode.admin

    def is_base(self) -> bool:
        return self == AppMode.base

    def is_cli(self) -> bool:
        return self == AppMode.cli

    def is_site(self) -> bool:
        return self == AppMode.site

    def is_worker(self) -> bool:
        return self == AppMode.worker


class ConfigurationError(Exception):
    pass


def init_app(app: Flask) -> None:
    app.extensions[EXTENSION_KEY] = {}

    app.byceps_app_mode = _determine_app_mode(app)

    if app.byceps_app_mode.is_site():
        if not app.config.get('SITE_ID'):
            raise ConfigurationError('No site ID configured.')


def _get_extension_value(key: str, app: Flask | None = None) -> Any:
    """Return the value for the key in this application's own extension
    namespace.

    It is expected that the value has already been set. An exception is
    raised if that is not the case.
    """
    if app is None:
        app = current_app

    extension = app.extensions[EXTENSION_KEY]
    return extension[key]


def _set_extension_value(key: str, value: Any, app: Flask) -> None:
    """Set/replace the value for the key in this application's own
    extension namespace.
    """
    extension = app.extensions[EXTENSION_KEY]
    extension[key] = value


# -------------------------------------------------------------------- #
# app mode


def _determine_app_mode(app: Flask) -> AppMode:
    value = app.config.get('APP_MODE')
    if value is None:
        return AppMode.base

    try:
        return AppMode[value]
    except KeyError as exc:
        raise ConfigurationError(
            f'Invalid app mode "{value}" configured.'
        ) from exc
