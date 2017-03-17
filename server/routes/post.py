from flask import jsonify, request
from server import app
from server.models.post import Post


@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts=Post.get_all_posts())


@app.route('/api/posts/<int:id>', methods=['GET'])
def get_post_by_id(id):
    post = Post.get_post_by_id(id)
    if post:
        return jsonify(post=post.serialize)
    else:
        return jsonify({
            "error": "Post not found with given net_id"
        })


@app.route('/api/posts', methods=['POST'])
def create_post():
    r = request.get_json(force=True)
    post = Post.create_post(
        professor_id=r.get('professor_id'),
        description=r.get('description'),
        qualifications=r.get('qualifications'),
        current_posts="",
        desired_skills="",
        capacity=1,
        current_number=0
    )
    return jsonify(post=post.serialize)


@app.route('/api/posts/<string:post_id>', methods=['DELETE'])
def delete_post(post_id):
    if Post.delete_post(post_id):
        return "Post deleted"
    else:
        return "Error in post deletion"
