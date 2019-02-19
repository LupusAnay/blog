from typing import List

from flask import Blueprint, jsonify, request, current_app

from app.models import Post, db, ValidationError

posts_blueprint = Blueprint('posts', __name__, url_prefix='/posts')


@posts_blueprint.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id: int):
    data = request.get_json()
    post: Post = Post.query.filter_by(id=post_id).first()

    if not post:
        return jsonify(status='error', message='no such entry'), 404

    if type(data) is not dict:
        return jsonify(status='error', message='wrong json'), 400

    try:
        post.update(**data)
    except ValidationError as exception:
        return jsonify(status='error', message=exception.message), 400

    db.session.commit()
    current_app.logger.debug(post.body)
    return '', 204


@posts_blueprint.route('/<int:post_id>', methods=['GET'])
def get_post(post_id: int):
    post: Post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify(status='error', message='no such entry'), 404
    return jsonify(post.as_dict()), 200


@posts_blueprint.route('', methods=['GET'])
def get_posts():
    posts: List[Post] = Post.query.all()
    return jsonify([post.as_dict() for post in posts]), 200


@posts_blueprint.route('', methods=['POST'])
def create_post():
    data: dict = request.get_json()

    if not data or type(data) is not dict:
        return jsonify(status='error', message='wrong json'), 400

    try:
        post: Post = Post(**data)
    except ValidationError as exception:
        current_app.logger.debug(
            f'Raised validation error: {exception.message}'
        )
        return jsonify(status='error', message=exception.message), 400

    current_app.logger.debug(f'Created Post entry: {post}')
    db.session.add(post)
    db.session.commit()
    return jsonify(id=post.id), 200
