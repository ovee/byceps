"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from .helpers import create_category, create_topic, find_topic


def test_move_topic(
    app, board_poster, moderator, moderator_client, category, another_category,
):
    topic_before = create_topic(category.id, board_poster.id)
    assert topic_before.category.id == category.id

    url = f'/board/topics/{topic_before.id}/move'
    form_data = {'category_id': another_category.id}
    response = moderator_client.post(url, data=form_data)

    assert response.status_code == 302

    topic_afterwards = find_topic(topic_before.id)
    assert topic_afterwards.category.id == another_category.id
