from flask import render_template, redirect
from flask import jsonify, request
from server import app
from config import TAGS, COURSES

# generate JS partials dynamically


@app.route('/js/<string:file_name>.js', methods=['GET'])
def js_create_post(file_name):
    if file_name == "create_post":
        return render_template(
            "js/createpost.js",
            all_tags=TAGS,
            all_courses=COURSES,
        )
    if file_name == "posts":
        net_id = request.args.get("net_id", "")
        if not str.isalnum(str(net_id)):
            return redirect('/', 302)

        return render_template(
            "js/posts.js",
            net_id=net_id
        )
    if file_name == "validate":
        return render_template(
            "js/validate.js"
        )
    else:
        return jsonify({
            "error": "professor with given net_id already exists"
        })
