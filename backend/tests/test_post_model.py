from app.models import Post, db
from tests.base_test_case import BaseTestCase


class TestPostModel(BaseTestCase):
    def test_post_as_dict(self):
        post: Post = Post(title='Hello', body='world')

        data: dict = post.as_dict()

        assert 'title' in data
        assert 'body' in data

        assert data['title'] is 'Hello'
        assert data['body'] is 'world'

    def test_update_from_dict(self):
        post: Post = Post(title='Hello', body='world')

        data: dict = {'title': 'Updated', 'body': 'dlrow'}

        post.update(data)
        updated_data = post.as_dict()

        assert 'title' in updated_data
        assert 'body' in updated_data

        assert updated_data['title'] is 'Updated'
        assert updated_data['body'] is 'dlrow'

    def test_as_dict_with_id(self, app):
        post: Post = Post(title='Hello', body='world')
        db.session.add(post)
        db.session.commit()
        data: dict = post.as_dict()

        assert post.id is 1
        assert 'id' in data
        assert data['id'] is 1
