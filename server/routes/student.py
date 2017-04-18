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
        name=r.get('name'),
        email=r.get('email'),
        password=r.get('password')
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


@app.route('/api/students/<string:net_id>', methods=['DELETE'])
def delete_student(net_id):
    if Student.delete_student(net_id):
        return "Student deleted"
    else:
        return jsonify({
            "error": "Could not delete student"
        })


# maybe a put request?
@app.route('/api/students/<string:net_id>/<int:post_id>', methods=['POST'])
def add_favorited_project(net_id, post_id):
    if Student.add_favorited_project(net_id, post_id):
        return "Added post to favorited posts"
    else:
        return jsonify({
            "error": "Could not add favorited post to student"
        })


@app.route('/api/students/<string:net_id>/<int:post_id>', methods=['DELETE'])
def delete_favorited_project(net_id, post_id):
    if Student.delete_favorited_project(net_id, post_id):
        return "Deleted post from favorited posts"
    else:
        return jsonify({
            "error": "Could not delete student"
        })
