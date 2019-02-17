from typing import List

from flask import Blueprint, jsonify, request

from app.models import Post, db

posts_blueprint = Blueprint('posts', __name__, url_prefix='/posts')


@posts_blueprint.route('', methods=['GET'])
def get_posts():
    posts: List[Post] = Post.query.all()
    return jsonify([post.as_dict() for post in posts]), 200


@posts_blueprint.route('', methods=['POST'])
def create_post():
    data: dict = request.get_json()
    post: Post = Post(**data)
    db.session.add(post)
    db.session.commit()
    return jsonify(id=post.id), 200
