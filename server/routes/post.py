from flask import jsonify, request
from server import app
from server.models.post import Post
from datetime import datetime
from flask_login import current_user, login_required


@app.route('/api/posts', methods=['POST'])
def create_post():
    """ An endpoint for creating a post to be used programmatically.
    This route is disabled except when the app is run with the debug flag.
    """
    if not app.debug:
        return jsonify(error="This endpoint is only enabled in debug mode.")

    r = request.get_json(force=True)
    post = Post.create_post(
        title=r.get('title'),
        professor_id=r.get('professor_id'),
        description=r.get('description'),
        tags=r.get('tags') or [],
        stale_date=r.get('stale_date') or datetime.now(),
        required_courses=r.get('required_courses') or [],
        project_link=r.get('project_link'),
        contact_email=r.get('contact_email')
    )
    return jsonify(post=post.serialize)


@app.route('/posts/<professor_id>/raw', methods=['GET'])
@login_required
def get_professor_posts_raw(professor_id):
    """ Returns a raw JSON of all posts for a given professor_id, only if the
    user is logged in and the professor whose posts were requestd.
    """
    if current_user.net_id == professor_id and \
            not current_user.is_student:
        return jsonify(
            professor_id=professor_id,
            posts=Post.get_posts(professor_id=professor_id)
        )
    else:
        return jsonify({})


@app.route('/raw/post-tags.json', methods=['GET'])
def get_post_tags_raw():
    return jsonify(tags=list(Post.TAGS))
