from flask import jsonify, request
from server import db, app
from server.models.user import User
from server.models.post import Post


# ROUTES FOR POSTS
# Get a json of all posts in the db
@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts=[p.serialize for p in Post.query.all()])


# Create a new post from the user
# Note: Do this by sending in {
#                               "post" : "<Hello, I had a question...>"
#                               } as a json
@app.route('/api/users/<string:email>/posts', methods=['POST'])
def create_post(email):
    user = User.query.filter(User.email == email).first()
    r = request.get_json(force=True)
    if user:
        post = Post(
            user_id=user.id,
            post=r.get("post", None)
        )
        user.create_post(post)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()
        return jsonify(messages=user.serialize_posts)
    else:
        return jsonify({
            "Error": "User Not Found"
            })


# Delete a post for the user
# Note: Do this by sending in {"post_id" : "<Post Id>" as a json
@app.route('/api/users/<string:email>/posts', methods=['DELETE'])
def delete_post(email):
    user = User.query.filter(User.email == email).first()
    r = request.get_json(force=True)
    if r.get('post_id'):
        post = Post.query.filter(Post.id == r.get('post_id')).first()
    if user:
        if post:
            if user.has_post(post):
                user.delete_post(post)
                db.session.add(user)
                db.session.commit()
                return jsonify(updated_posts=user.serialize_posts)
            else:
                return jsonify({"Error": "Post does not exist!"})
        else:
            return jsonify({
                "Error": "Post Not Found"
                })
    else:
        return jsonify({
            "Error": "User Not Found"
            })
