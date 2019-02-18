from typing import List

from flask import Blueprint, jsonify, request, current_app

from app.models import Post, db, ValidationError

posts_blueprint = Blueprint('posts', __name__, url_prefix='/posts')


@posts_blueprint.route('', methods=['GET'])
def get_posts():
    posts: List[Post] = Post.query.all()
    return jsonify([post.as_dict() for post in posts]), 200


@posts_blueprint.route('', methods=['POST'])
def create_post():
    data: dict = request.get_json()

    if not data:
        return jsonify(status='error', message='wrong json'), 400

    try:
        post: Post = Post(**data)
    except ValidationError as e:
        current_app.logger.debug(f'Raised validation error: {e.message}')
        return jsonify(status='error', message=e.message), 400

    current_app.logger.debug(f'Created Post entry: {post}')
    db.session.add(post)
    db.session.commit()
    return jsonify(id=post.id), 200
