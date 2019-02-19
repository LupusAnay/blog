from typing import List, Dict

from flask import Response

from app.models import Post, db
from tests.base_test_case import BaseTestCase


class TestPostsView(BaseTestCase):
    def test_get_method(self, client):
        posts: List[Post] = [Post(title=str(x), body=str(x)) for x in
                             range(100)]
        [db.session.add(post) for post in posts]
        db.session.commit()
        response: Response = client.get('/posts')

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.get_json()

        assert data
        assert len(data) == 100

    def test_post_method(self, client):
        data = {'title': 'Hello', 'body': 'World'}

        response: Response = client.post('/posts', json=data)

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        response_data = response.get_json()

        assert response_data
        assert 'id' in response_data
        assert response_data['id'] == 1

        post: Post = Post.query.filter_by(id=response_data['id']).first()

        assert post.id == 1
        assert post.title == 'Hello'
        assert post.body == 'World'

    def test_post_method_without_data(self, client):
        response: Response = client.post('/posts')

        assert response.status_code == 400

        data = response.get_json()

        assert data
        assert 'status' in data
        assert 'message' in data
        assert data.get('status') == 'error'

    def test_post_method_with_invalid_data(self, client):
        data_array = {
            'Empty data': None,
            'Invalid keys': {'foo': 'bar', 'baz': 'qux'},
            'Non dictionary': 'hello',
            'Empty values': {'title': '', 'body': ''},
            'Spaces': {'title': ' ', 'body': ' '},
            'Numbers': {'title': 1, 'body': 2},
            'Redundant keys': {'title': 'foo', 'body': 'bar', 'baz': 'qux'}
        }

        responses: Dict[str, Response] = {}

        for name, data in data_array.items():
            responses[name] = (client.post(f'/posts', json=data))

        for name, response in responses.items():
            assert response.status_code == 400, \
                f'Assertion failed on `{name}` data'

            data = response.get_json()

            assert data
            assert 'status' in data
            assert 'message' in data
            assert data.get('status') == 'error'

    def test_get_by_id(self, client):
        post: Post = Post(title='foo', body='bar')
        db.session.add(post)
        db.session.commit()

        response: Response = client.get(f'/posts/{post.id}')

        assert response.status_code == 200

        data: dict = response.get_json()

        assert data
        assert 'id' in data
        assert 'title' in data
        assert 'body' in data
        assert data['id'] == post.id
        assert data['body'] == post.body
        assert data['title'] == post.title

    def test_get_by_id_with_invalid_id(self, client):
        response: Response = client.get('/posts/65')

        assert response.status_code == 404

        data = response.get_json()

        assert data
        assert 'status' in data
        assert 'message' in data
        assert data.get('status') == 'error'

    def test_put_method(self, client):
        post: Post = Post(title='foo', body='bar')
        db.session.add(post)
        db.session.commit()

        data = {'title': 'Updated', 'body': 'dlroW'}

        response: Response = client.put(f'/posts/{post.id}', json=data)

        post = Post.query.filter_by(id=post.id).first()

        assert response.status_code == 204

        assert post.body == data['body']
        assert post.title == data['title']

    def test_put_method_with_invalid_id(self, client):
        updated_data = {'title': 'Updated', 'body': 'dlroW'}

        response: Response = client.put('/posts/65', json=updated_data)

        assert response.status_code == 404

        data = response.get_json()

        assert data
        assert 'status' in data
        assert 'message' in data
        assert data.get('status') == 'error'

    def test_put_method_without_data(self, client):
        post: Post = Post(title='foo', body='bar')
        db.session.add(post)
        db.session.commit()

        response: Response = client.put(f'/posts/{post.id}')

        assert response.status_code == 400

        data = response.get_json()

        assert data
        assert 'status' in data
        assert 'message' in data
        assert data.get('status') == 'error'

    def test_put_method_with_invalid_data(self, client):
        post: Post = Post(title='foo', body='bar')
        db.session.add(post)
        db.session.commit()

        data_array = {
            'Empty data': None,
            'Invalid keys': {'foo': 'bar', 'baz': 'qux'},
            'Non dictionary': 'hello',
            'Empty values': {'title': '', 'body': ''},
            'Spaces': {'title': ' ', 'body': ' '},
            'Numbers': {'title': 1, 'body': 2},
            'Redundant keys': {'title': 'foo', 'body': 'bar', 'baz': 'qux'}
        }

        responses: Dict[str, Response] = {}

        for name, data in data_array.items():
            responses[name] = client.put(f'/posts/{post.id}', json=data)

        for name, response in responses.items():
            assert response.status_code == 400, \
                f'Assertion failed on `{name}` data'

            data = response.get_json()

            assert data
            assert 'status' in data
            assert 'message' in data
            assert data.get('status') == 'error'

    def test_delete_method(self, client):
        post: Post = Post(title='foo', body='bar')
        db.session.add(post)
        db.session.commit()

        response: Response = client.delete(f'/posts/{post.id}')

        assert response.status_code == 204

    def test_delete_method_with_invalid_id(self, client):
        response: Response = client.delete('/posts/65')

        data = response.get_json()
        assert response.status_code == 404
        assert data
        assert 'status' in data
        assert 'message' in data
        assert data['status'] == 'error'
