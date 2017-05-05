from flask import render_template, flash, redirect, request
from server import app
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from models import Post, Student, Professor
from werkzeug import secure_filename
from config import BASE_URL
import os


@app.route('/')
@app.route('/index')
@app.route('/posts')
@app.route('/posts/')
@app.route('/page/<int:page>')
@app.route('/posts/tags=<tags>')
@app.route('/posts/tags=<tags>/<all>')
@login_required
def index(tags=None, all=None, posts=None, page=None):
    page = page if page else 1

    if tags:
        tags = tags.lower().strip().split(',')

    if posts is None:
        posts, has_next = Post.get_compressed_posts(
            page=page,
            tags=tags, exclusive=True if all == 'all' else False)
    for post in posts:
        post['professor_name'] = Professor.get_professor_by_netid(
            post['professor_id']).name

    posts.sort(key=lambda x: x['date_created'], reverse=True)
    return render_template(
        "index.html",
        title='Home',
        url=BASE_URL,
        user=current_user,
        posts=posts,
        search=True,
        isInIndex=True,
        tags=Post.TAGS if tags is None else tags,
        page=page,
        has_next_page=has_next
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = (Professor.query.filter_by(email=form.email.data).first() or
                Student.query.filter_by(email=form.email.data).first())
        if user:
            if user.is_correct_password(form.password.data):
                login_user(user)
                flash('Welcome back %s!' % user.name)
                next = request.args.get('next')
                return redirect(next or '/index')
            else:
                flash('Username or Password Incorrect!')
                return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/profile/<net_id>', methods=['GET', 'POST'])
@login_required
def profile(net_id):
    favorited_projects = Student.get_student_favorited_projects(net_id)
    post_collection = Post.get_posts_by_professor_id(net_id)
    for post in post_collection:
        post['professor_name'] = Professor.get_professor_by_netid(
            post['professor_id']).name
    if request.method == 'POST':
        result = request.form
        if current_user.is_student:
            user = Student.get_student_by_netid(net_id)
            new_email = result["user_email"] or (net_id + "@cornell.edu")
            new_year = result["user_year"] or "Freshman"
            new_description = result["user_description"] or " "
            interests = result["profile_interests"] or " "
            skills = result["profile_skills"] or " "
            availability = ','.join(result.getlist("weekday"))
            f = request.files['resume']
            if f:
                if allowed_file(f.filename):
                    extension = f.filename.rsplit('.', 1)[1]
                    f.filename = net_id + "_resume." + extension
                    filename = secure_filename(f.filename)
                    f.save(os.path.join('uploads/', filename))
                else:
                    flash('Resume File Type Not Accepted')
                    filename = None
            else:
                filename = None
            Student.update_student(
                net_id, email=new_email, name=None, major=user.major,
                year=new_year,
                skills=skills, resume=filename, description=new_description,
                interests=interests, favorited_projects=None,
                availability=availability
            )
        else:
            new_email = result["user_email"] or (net_id + "@cornell.edu")
            new_description = result["user_description"] or "no bio"
            new_interests = result["profile_interests"] or " "
            Professor.update_professor(
                net_id, name=None, email=new_email,
                desc=new_description, interests=new_interests
            )
        return redirect("/profile/" + net_id, code=302)
    else:
        return render_template(
            'profile.html',
            title=current_user.name + "'s Profile",
            profile=current_user,
            favorited_projects=favorited_projects,
            post_collection=post_collection
        )


@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def createpost():
    if current_user.is_student:
        return redirect('/index')

    if request.method == 'POST':
        result = request.form
        print(result)
        Post.create_post(
            result["post_title"],
            result["post_description"],
            current_user.net_id,
            result['tags'].lower().strip().split(','),
            '',  # qualifications
            '',  # desired skills
            None if result['stale-days'] == '-1' else int(result['stale-days']),
            result['post_professor_email'],
            result['project-link'],
            '',  # required courses
            ''  # grad_only
        )
        return redirect("/posts", code=302)
    else:
        return render_template(
            'createpost.html',
            title='Submit Research Listing',
            tags=Post.TAGS,
            post=Post.empty
        )


@app.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def showpost(post_id):
    post = Post.get_post_by_id(post_id)
    if not post:
        return redirect('/index')

    post = post.serialize
    post['professor_name'] = Professor.get_professor_by_netid(
        post['professor_id']).name
    return render_template(
        'full_post.html',
        post=post
    )


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    post = Post.get_post_by_id(post_id)
    if not post:
        return redirect('/index')

    if request.method == 'POST':
        result = request.form
        Post.update_post(
            post_id,
            description=result['post_description'],
            tags=result['tags'].split(','),
            title=result['post_title'],
            contact_email=result['post_professor_email'],
            project_link=result['project-link']
        )
        return redirect('/posts/%s' % post_id)
    else:
        post = post.serialize
        post['tags'] = ",".join(post['tags'])
        return render_template(
            'createpost.html',
            id='Sign In',
            post=post
        )


@app.route('/styleguide', methods=['GET'])
def get_styleguide():
    return render_template(
        'styleguide.html'
    )

# move to apis
@app.route('/search', methods=['GET'])
def search():
    print("ok")
    if request.method == 'GET':
        result = request.args
        posts = Post.search(
            is_grad=result['graduate_research'],
            taken_courses=result['desired_courses'],
            tags=result['tags'] or None,
            keywords=result['keywords'] or None
        )
        for post in posts:
            post['professor_name'] = Professor.get_professor_by_netid(
                post['professor_id']).name
        print(posts)
        posts.sort(key=lambda x: x['id'], reverse=True)

        from flask import jsonify
        rendered_posts = []
        for p in posts:
            rendered_posts.append(render_template("partials/post.html", 
                post=p,
                isInIndex=True,
                user=current_user))
        return jsonify({
            "rendered_posts": rendered_posts
        })


@app.errorhandler(413)
def page_not_found(e):
    flash('Resume File Size Exceeds Limit')
    return redirect("/profile/" + current_user.net_id, code=302)
