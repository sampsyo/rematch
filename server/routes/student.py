from flask import jsonify, request
from server import app
from server.models.student import Student


@app.route('/api/students', methods=['POST'])
def create_student():
    """ An endpoint for creating a student to be used programmatically.
    This route is disabled except when the app is run with the debug flag.
    """
    if not app.debug:
        return jsonify(error="This endpoint is only enabled in debug mode.")

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


# Add starred post to student profile
@app.route('/api/students/<string:net_id>/<int:post_id>', methods=['POST'])
def add_favorited_project(net_id, post_id):
    """ Add a starred post to a student profile. """
    if Student.add_favorited_project(net_id, post_id):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})


@app.route('/api/students/<string:net_id>/<int:post_id>', methods=['DELETE'])
def delete_favorited_project(net_id, post_id):
    """ Remove a starred post from a student profile. """
    if Student.delete_favorited_project(net_id, post_id):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"})
