from flask import jsonify, request
from server import app
from server.models.post import Post


@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts=Post.get_all_posts())


@app.route('/api/posts/<int:id>', methods=['GET'])
def get_post_by_id(post_id):
    post = Post.get_post_by_id(post_id)
    if post:
        return jsonify(post=post.serialize)
    else:
        return jsonify({
            "error": "Post not found with given id"
        })


@app.route('/api/posts', methods=['POST'])
def create_post():
    r = request.get_json(force=True)
    post = Post.create_post(
        title=r.get('title'),
        professor_id=r.get('professor_id'),
        description=r.get('description'),
        qualifications=r.get('qualifications'),
        current_students="",
        desired_skills="",
        capacity=1,
        current_number=0
    )
    return jsonify(post=post.serialize)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    if Post.delete_post(post_id):
        return "Post deleted"
    else:
        return jsonify({
            "error": "Post not deleted"
        })


@app.route('/api/posts', methods=['POST'])
def update_post():
    r = request.get_json(force=True)
    post = Post.update_post(
        r.get('id', None),
        r.get('title', None),
        r.get('description', None),
        r.get('qualifications', None),
        r.get('professor_id', None),
        r.get('current_students', None),
        r.get('desired_skills', None),
        r.get('capacity', None),
        r.get('current_number', None)
    )
    if not post:
        return jsonify({
            "error": "Post not found"
        })
    return jsonify(post=post.serialize)
