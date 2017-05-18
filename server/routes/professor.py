from flask import jsonify, request
from server import app
from server.models.professor import Professor

# Returns a Response object of all professors from the database
@app.route('/api/professors', methods=['GET'])
def get_all_professors():
    return jsonify(professors=Professor.get_all_professors())


# Add a new user to the database 
# Return a Response object if valid professor
@app.route('/api/professors', methods=['POST'])
def create_professor():
    r = request.get_json(force=True)
    professor = Professor.create_professor(
        net_id=r.get('net_id'),
        name=r.get('name'),
        email=r.get('email'),
        password=r.get('password')
    )
    if professor:
        return jsonify(professor=professor.serialize)
    else:
        return jsonify({
            "error": "professor with given net_id already exists"
        })


# Return a Response object given valid professor netid
@app.route('/api/professors/<string:net_id>', methods=['GET'])
def get_professor_by_netid(net_id):
    professor = Professor.get_professor_by_netid(net_id)
    if professor:
        return jsonify(professor=professor.serialize)
    else:
        return jsonify({
            "error": "User not found with given net_id"
        })

# If valid student netid, delete corresponding professor from database
@app.route('/api/professors/<string:net_id>', methods=['DELETE'])
def delete_professor(net_id):
    if Professor.delete_professor(net_id):
        return "professor deleted"
    else:
        return jsonify({
            "error": "Could not delete professor"
        })
