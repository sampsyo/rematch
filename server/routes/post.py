from flask import jsonify, request
from server import db, app
from server.models.post import Post


@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(students=Post.get_all_posts())


@app.route('/api/posts', methods=['POST'])
def create_post():
    r = request.get_json(force=True)
    post = Post.create_post(
        description=r.get('description'),
        qualifications=r.get('qualifications'),
        professor_id=r.get('professor_id'),
        current_students="",
        desired_skills="",
        capacity=1,
        current_number=0
    )
    return jsonify(post=post.serialize)
#
#
## Delete a post for the user
## Note: Do this by sending in {"post_id" : "<Post Id>" as a json
#@app.route('/api/users/<string:email>/posts', methods=['DELETE'])
#def delete_post(email):
#    user = User.query.filter(User.email == email).first()
#    r = request.get_json(force=True)
#    if r.get('post_id'):
#        post = Post.query.filter(Post.id == r.get('post_id')).first()
#    if user:
#        if post:
#            if user.has_post(post):
#                user.delete_post(post)
#                db.session.add(user)
#                db.session.commit()
#                return jsonify(updated_posts=user.serialize_posts)
#            else:
#                return jsonify({"Error": "Post does not exist!"})
#        else:
#            return jsonify({
#                "Error": "Post Not Found"
#                })
#    else:
#        return jsonify({
#            "Error": "User Not Found"
#            })
