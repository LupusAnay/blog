from typing import List

from flask import Response

from app.models import Post, db
from tests.base_test_case import BaseTestCase


class TestPostsView(BaseTestCase):
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

    def test_post_method(self, client):
        data = {'title': 'Hello', 'body': 'World'}

        response: Response = client.post('/posts', json=data)

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.get_json()
        assert 'id' in response.get_json()
        assert response.get_json()['id'] == 1

        post: Post = Post.query.filter_by(id=response.get_json()['id']).first()

        assert post.id == 1
        assert post.title == 'Hello'
        assert post.body == 'World'

    def test_post_method_with_invalid_json(self, client):
        data = {}

        response: Response = client.post('/posts', json=data)

        assert response.status_code == 400
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'

    def test_post_method_without_data(self, client):
        response: Response = client.post('/posts')

        assert response.status_code == 400
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'

    def test_post_method_with_empty_values(self, client):
        data = {'title': '', 'body': ''}

        response: Response = client.post('/posts', json=data)

        assert response.status_code == 400
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'

    def test_post_method_with_spaces_values(self, client):
        data = {'title': '    ', 'body': '  '}

        response: Response = client.post('/posts', json=data)

        assert response.status_code == 400
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'

    def test_post_method_with_numbers_values(self, client):
        data = {'title': 1, 'body': 0}

        response: Response = client.post('/posts', json=data)

        assert response.status_code == 400
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'

    def test_post_method_with_bigger_json(self, client):
        # Not sure about desired behavior here, should model complain about
        # extra attributes, or just ignore it
        # for this moment - ignore is desired

        data = {'title': 'hello', 'body': 'world', 'title1': 'hello'}

        response: Response = client.post('/posts', json=data)
        assert response.status_code == 400
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'
