from flask import jsonify, request
from server import db, app
from server.models.user import User


# ROUTES FOR USER
# Get a json of all users in the db
@app.route('/api/users', methods=['GET'])
def get_all_users():
    return jsonify(users=[i.serialize for i in User.query.all()])


# Add a new user to the database
@app.route('/api/users', methods=['POST'])
def add_new_user():
    # Gets the new user attempts
    r = request.get_json(force=True)
    # Converts json into a User instance
    user = User(
        email=r.get('email', None),
        name=r.get('name', None)
    )
    db.session.add(user)
    db.session.commit()

#    # Not sure how a user would be initialized with posts but..just in case?
#    for posts in (r.get('posts', [])):
#        id_num = posts.get('id', "")
#        a = Post.query.get(id_num)
#        # Tries it by the id number
#        if a:
#            user.create_post(a)
#
#    # Re commits additions to user
#    db.session.add(user)
#    db.session.commit()
    return jsonify(new_user=user.serialize)


# Search users by their unique identifier (Email in this case)
@app.route('/api/users/<string:email>', methods=['GET'])
def get_single_user(email):
    user = User.query.filter(User.email == email).first()
    if user:
        return jsonify(user=user.serialize)
    else:
        return jsonify({
            "Error": "User Not Found"
        })


# Edit a users profile
@app.route('/api/users/<string:email>', methods=['PUT'])
def edit_user(email):
    user = User.query.filter(User.email == email).first()

    # Gets the new user attempts
    r = request.get_json(force=True)
    user.email = r.get('email', user.email)
    user.name = r.get('name', user.name)

    db.session.add(user)
    db.session.commit()
    return jsonify(updated_user=user.serialize)


# Remove a user from the database
@app.route('/api/users/<string:email>', methods=['DELETE'])
def remove_user(email):
    user = User.query.filter(User.email == email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return jsonify(updated_users=[i.serialize for i in User.query.all()])


# Get a set of all users posts
@app.route('/api/users/<string:email>/posts', methods=['GET'])
def get_all_users_posts(email):
    user = User.query.filter(User.email == email).first()
    if user:
        return jsonify(posts=user.serialize_posts)
    else:
        return jsonify({
            "Error": "User Not Found"
        })
