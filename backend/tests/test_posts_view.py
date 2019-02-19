from typing import List

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
        assert response.get_json()
        assert len(response.get_json()) == 100

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
        data = {'title': 'hello', 'body': 'world', 'title1': 'hello'}

        response: Response = client.post('/posts', json=data)
        assert response.status_code == 400
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'

    def test_get_by_id(self, client):
        data = {'title': 'Hello', 'body': 'World'}

        create_response: Response = client.post('/posts', json=data)

        assert create_response.status_code == 200
        assert 'id' in create_response.get_json()

        post_id = create_response.get_json().get('id')
        response: Response = client.get(f'/posts/{post_id}')

        assert response.status_code == 200
        assert response.get_json()
        assert 'id' in response.get_json()
        assert 'title' in response.get_json()
        assert 'body' in response.get_json()
        assert response.get_json()['id'] == post_id
        assert response.get_json()['body'] == data['body']
        assert response.get_json()['title'] == data['title']

    def test_get_by_id_with_invalid_id(self, client):
        response: Response = client.get('/posts/65')

        assert response.status_code == 404
        assert response.get_json()
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()
        assert response.get_json().get('status') == 'error'

    def test_put_method(self, client):
        data = {'title': 'Hello', 'body': 'World'}

        create_response: Response = client.post('/posts', json=data)

        assert create_response.status_code == 200
        assert 'id' in create_response.get_json()
        post_id = create_response.get_json().get('id')

        updated_data = {'title': 'Updated', 'body': 'dlroW'}

        response: Response = client.put(f'/posts/{post_id}', json=updated_data)

        assert response.status_code == 204

        updated_post: Response = client.get(f'/posts/{post_id}')

        assert updated_post.status_code == 200
        assert updated_post.get_json()
        assert 'id' in updated_post.get_json()
        assert 'title' in updated_post.get_json()
        assert 'body' in updated_post.get_json()
        assert updated_post.get_json()['id'] == post_id
        assert updated_post.get_json()['body'] == updated_data['body']
        assert updated_post.get_json()['title'] == updated_data['title']
