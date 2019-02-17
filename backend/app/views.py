from typing import List

from flask import Blueprint, jsonify, current_app

from app.models import Post

posts_blueprint = Blueprint('posts', __name__, url_prefix='/posts')


@posts_blueprint.route('', methods=['GET'])
def get_posts():
    posts: List[Post] = Post.query.all()
    current_app.logger.debug(posts)
    current_app.logger.debug([post.as_dict() for post in posts])
    return jsonify([post.as_dict() for post in posts]), 200
