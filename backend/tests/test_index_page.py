from typing import List

from flask import Response

from app.models import Post, db
from tests.base_test_case import BaseTestCase


class TestIndexPage(BaseTestCase):
    def test_get_method(self, client):
        posts: List[Post] = [Post(title=str(x), body=str(x)) for x in
                             range(1, 100)]
        [db.session.add(post) for post in posts]
        db.session.commit()
        response: Response = client.get('/posts')

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.get_json()
        assert len(response.get_json()) == 99

