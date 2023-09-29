"""
byceps.services.gallery.gallery_domain_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations

from datetime import datetime

from byceps.typing import BrandID
from byceps.util.uuid import generate_uuid4, generate_uuid7

from .models import (
    Gallery,
    GalleryID,
    GalleryImage,
    GalleryImageID,
)


def create_gallery(
    brand_id: BrandID,
    slug: str,
    title: str,
    hidden: bool,
) -> Gallery:
    """Create a gallery."""
    gallery_id = GalleryID(generate_uuid4())

    return Gallery(
        id=gallery_id,
        created_at=datetime.utcnow(),
        brand_id=brand_id,
        slug=slug,
        title=title,
        title_image=None,
        position=0,
        hidden=hidden,
    )


def create_image(
    gallery_id: GalleryID,
    caption: str | None,
    hidden: bool,
) -> GalleryImage:
    """Create a gallery image."""
    image_id = GalleryImageID(generate_uuid7())

    return GalleryImage(
        id=image_id,
        created_at=datetime.utcnow(),
        gallery_id=gallery_id,
        caption=caption,
        position=0,
        hidden=hidden,
    )