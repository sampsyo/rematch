from flask import render_template, flash, redirect, request
from server import app
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template_string
from models import Post, Student, Professor


@app.route('/')
@app.route('/index')
@app.route('/posts')
@app.route('/posts/')
@app.route('/posts/tags=<tags>')
@app.route('/posts/tags=<tags>/<all>')
# I need to know the netid of the student here so I can get back the
# favorited_projects for them on the search / home page.
@login_required
def index(tags=None, all=None):
    if tags:
        tags = tags.lower().strip().split(',')
    posts = Post.get_compressed_posts(tags=tags, exclusive=True if
                                      all == 'all' else False)
    return render_template(
        "index.html",
        title='Home',
        user=current_user,
        posts=posts,
        search=True,
        isInIndex=True
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
    flash('Username or Password Incorrect!')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


@app.route('/profile/<net_id>', methods=['GET', 'POST'])
@login_required
def profile(net_id):
    favorited_projects = Student.get_student_favorited_projects(net_id)
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
            # Flask fileupload ?
            resume = result["resume"]
            Student.update_student(
                net_id, email=new_email, name=None, major=user.major,
                year=new_year,
                skills=skills, resume=resume, description=new_description,
                interests=interests, favorited_projects=None,
                availability=availability
            )
        else:
            new_email = result["user_email"] or (net_id + "@cornell.edu")
            new_description = result["user_description"] or "no bio"
            Professor.update_professor(
                net_id, name=None, email=new_email,
                desc=new_description, interests=None
            )
        return redirect("/profile/" + net_id, code=302)
    else:
        return render_template(
          'profile.html',
          title=current_user.name + "'s Profile",
          profile=current_user,
          favorited_projects=favorited_projects
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
            None if result['stale-days'] == '-1' else int(result['stale-days'])
        )
        return redirect("/posts", code=302)
    else:
        return render_template(
            'createpost.html',
            title='Submit Research Listing',
            tags=Post.TAGS
        )


@app.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def showpost(post_id):
    post = Post.get_post_by_id(post_id)
    return render_template(
        'post.html',
        post=post.serialize
    )


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    if request.method == 'POST':
        result = request.form
        return render_template_string(
            "{{ result.title }} result {{ result.description }}",
            result=result
        )
    else:
        return render_template(
            'createpost.html',
            id='Sign In'
        )


@app.route('/styleguide', methods=['GET'])
def get_styleguide():
    return render_template(
        'styleguide.html'
    )
