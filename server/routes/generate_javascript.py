from flask import render_template
from flask import jsonify, request
from server import app
from server.models.post import Post

# generate JS partials dynamically

@app.route('/js/<string:file_name>.js', methods=['GET'])
def js_create_post(file_name):
    if file_name == "create_post":
        return render_template(
            "js/createpost.js",
            all_tags=Post.TAGS,
            all_courses=Post.COURSES
        )
    if file_name == "posts":
        return render_template(
            "js/posts.js"
        )
    else:
        return jsonify({
            "error": "professor with given net_id already exists"
        })