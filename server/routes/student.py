from flask import jsonify, request
from server import app
from server.models.student import Student


@app.route('/api/students', methods=['GET'])
def get_all_students():
    return jsonify(students=Student.get_all_students())


# Add a new user to the database
@app.route('/api/students', methods=['POST'])
def create_student():
    r = request.get_json(force=True)
    student = Student.create_student(
        net_id=r.get('net_id'),
        name=r.get('name')
    )
    if student:
        return jsonify(student=student.serialize)
    else:
        return jsonify({
            "error": "Student with given net_id already exists"
        })


@app.route('/api/students/<string:net_id>', methods=['GET'])
def get_student_by_netid(net_id):
    student = Student.get_student_by_netid(net_id)
    if student:
        return jsonify(student=student.serialize)
    else:
        return jsonify({
            "error": "User not found with given net_id"
        })


# Edit a users profile
#@app.route('/api/users/<string:email>', methods=['PUT'])
#def edit_user(email):
#    user = User.query.filter(User.email == email).first()
#
#    # Gets the new user attempts
#    r = request.get_json(force=True)
#    user.email = r.get('email', user.email)
#    user.name = r.get('name', user.name)
#
#    db.session.add(user)
#    db.session.commit()
#    return jsonify(updated_user=user.serialize)
#
#
## Remove a user from the database
#@app.route('/api/users/<string:email>', methods=['DELETE'])
#def remove_user(email):
#    user = User.query.filter(User.email == email).first()
#    if user:
#        db.session.delete(user)
#        db.session.commit()
#    return jsonify(updated_users=[i.serialize for i in User.query.all()])
#
#
## Get a set of all users posts
#@app.route('/api/users/<string:email>/posts', methods=['GET'])
#def get_all_users_posts(email):
#    user = User.query.filter(User.email == email).first()
#    if user:
#        return jsonify(posts=user.serialize_posts)
#    else:
#        return jsonify({
#            "Error": "User Not Found"
#        })
