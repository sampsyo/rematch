from flask import jsonify, request
from server import app
from server.models.post import Post


@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts=Post.get_posts())


@app.route('/api/posts/tags=<tags>/all', methods=['GET'])
def get_posts_exclusive(tags):
    tags = tags.lower().split(',')
    return jsonify(posts=Post.get_posts(tags=tags, exclusive=True))


@app.route('/api/posts/tags=<tags>', methods=['GET'])
def get_posts_inclusive(tags):
    tags = tags.lower().split(',')
    return jsonify(posts=Post.get_posts(tags=tags, exclusive=False))


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
        tags=r.get('tags'),
        qualifications='',
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


@app.route('/api/posts/<int:post_id>', methods=['POST'])
def update_post(post_id):
    r = request.get_json(force=True)
    post = Post.update_post(
        post_id,
        capacity=r.get('capacity', None),
        current_number=r.get('current_number', None),
        current_students=r.get('current_students', None),
        description=r.get('description', None),
        desired_skills=r.get('desired_skills', None),
        is_active=r.get('is_active', None),
        professor_id=r.get('professor_id', None),
        qualifications=r.get('qualifications', None),
        tags=r.get('tags', None),
        title=r.get('title', None)
    )
    if not post:
        return jsonify({
            "error": "Post not found"
        })
    return jsonify(post=post.serialize)


@app.route('/posts/<professor_id>/raw', methods=['GET'])
def get_professor_posts_raw(professor_id):
    return jsonify(
        professor_id=professor_id,
        posts=Post.get_posts_by_professor_id(professor_id)
    )
