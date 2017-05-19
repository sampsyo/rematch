from flask import jsonify, request
from server import app
from server.models.professor import Professor


@app.route('/api/professors', methods=['POST'])
def create_professor():
    """ An endpoint for creating a professor to be used programmatically.
    This route is disabled except when the app is run with the debug flag.
    """
    if not app.debug:
        return jsonify(error="This endpoint is only enabled in debug mode.")

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
