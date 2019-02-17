from app.models import Post, db
from tests.base_test_case import BaseTestCase


class TestPostModel(BaseTestCase):
    def test_post_as_dict(self):
        post: Post = Post(title='Hello', body='world')

        data: dict = post.as_dict()

        assert 'title' in data
        assert 'body' in data

        assert data['title'] == 'Hello'
        assert data['body'] == 'world'

    def test_update_from_dict(self):
        post: Post = Post(title='Hello', body='world')

        data: dict = {'title': 'Updated', 'body': 'dlrow'}

        post.update(data)
        updated_data = post.as_dict()

        assert 'title' in updated_data
        assert 'body' in updated_data

        assert updated_data['title'] == 'Updated'
        assert updated_data['body'] == 'dlrow'

    def test_as_dict_with_id(self, app):
        post: Post = Post(title='Hello', body='world')
        db.session.add(post)
        db.session.commit()
        data: dict = post.as_dict()

        assert post.id == 1

        assert 'id' in data
        assert 'title' in data
        assert 'body' in data

        assert data['id'] == 1
        assert data['title'] == 'Hello'
        assert data['body'] == 'world'
