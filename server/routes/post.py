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


@app.route('/api/setpostinactive/<int:post_id>', methods=['GET'])
def setpostinactive(post_id):
    post = Post.get_post_by_id(post_id)
    if post:
        post = Post.update_post(
            post_id,
            description=None, desired_skills=None, is_active=False,
                    professor_id=None, qualifications=None, required_courses=None,
                    tags=None, title=None, project_link=None, contact_email=None,
                    grad_only=None
        )
        return jsonify(post=post.serialize)
    else:
        return jsonify({
            "error": "Post not found with given id"
        })

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
        desired_skills="",
        stale_days=10,
        grad_only=False,
        required_courses="",
        project_link="",
        contact_email=""
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
        description=r.get('description', None),
        desired_skills=r.get('desired_skills', None),
        is_active=r.get('is_active', False),
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


@app.route('/raw/post-tags.json', methods=['GET'])
def get_post_tags_raw():
    return jsonify(tags=list(Post.TAGS))


@app.route('/search', methods=['GET'])
def search():
    print("ok")
    if request.method == 'GET':
        result = request.args
        posts = Post.get_posts(
            page=1,
            compressed=True,
            # taken_courses=result['desired_courses'],
            tags=result['tags'] or None,
            keywords=result['keywords'] or None
        )
        for post in posts:
            post['professor_name'] = Professor.get_professor_by_netid(
                post['professor_id']).name
        print(posts)

        from flask import jsonify
        rendered_posts = []
        for p in posts:
            rendered_posts.append(render_template("partials/post.html", 
                post=p,
                isInIndex=True,
                user=current_user))
        return jsonify({
            "rendered_posts": rendered_posts
        })
