from flask import render_template, flash, redirect, request
from server import app
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from models import Post, Student, Professor
from werkzeug import secure_filename
from config import BASE_URL, TAGS, COURSES
import os
import datetime


@app.route('/', methods=['GET'])
@app.route('/posts', methods=['GET'])
@login_required
def posts():
    phrase = request.args.get('phrase', None)
    search_tags = request.args.get('search_tags', None)
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    courses = current_user.is_student and request.args.get('courses', False)

    url_params = []
    if search_tags:
        url_params.append('search_tags=%s' % search_tags)
    if phrase:
        url_params.append('phrase=%s' % phrase)
    if courses:
        url_params.append('courses=%s' % courses.lower())
    search_url = '&%s' % '&'.join(url_params)

    posts, has_next, total_number_of_pages = Post.get_posts(
        page=page, compressed=True, tags=search_tags, keywords=phrase,
        active_only=True,
        required_courses=current_user.courses if bool(courses) else None
    )
    Professor.annotate_posts(posts)

    return render_template(
        "index.html",
        title='Home',
        user=current_user,
        base_url=BASE_URL,
        posts=posts,
        search=True,
        isInIndex=True,
        tags=TAGS,
        total_number_of_pages=total_number_of_pages,
        search_tags=search_tags or '',
        checked='checked' if bool(courses) else '',
        page=page,
        phrase=phrase or '',
        has_next_page=has_next,
        search_url=search_url
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
                return redirect(next or BASE_URL)
            else:
                flash('Username or Password Incorrect!')
                return redirect('/login')
    return render_template(
        'login.html',
        base_url=BASE_URL,
        form=form
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(BASE_URL)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/profile/<net_id>', methods=['GET'])
@login_required
def profile(net_id):
    if not current_user.net_id == net_id:
        return redirect("/", code=301)

    favorited_projects = None
    active_collection = None
    inactive_collection = None

    if current_user.is_student:
        favorited_projects = Student.get_student_favorited_projects(net_id)
        Professor.annotate_posts(favorited_projects)
    else:
        active_collection, _, _ = Post.get_posts(
            professor_id=net_id, active_only=True, compressed=True)
        inactive_collection, _, _ = Post.get_posts(
            professor_id=net_id, inactive_only=True, compressed=True)

        Professor.annotate_posts(active_collection)
        Professor.annotate_posts(inactive_collection)

    return render_template(
        'profile.html',
        title=current_user.name + "'s Profile",
        base_url=BASE_URL,
        profile=current_user,
        isInIndex=True,
        all_courses=COURSES,
        favorited_projects=favorited_projects,
        active_collection=active_collection,
        inactive_collection=inactive_collection
    )


@app.route('/profile/<net_id>', methods=['POST'])
@login_required
def profile_update(net_id):
    if not current_user.net_id == net_id:
        return redirect("/", code=301)

    result = request.form
    if current_user.is_student:
        user = Student.get_student_by_netid(net_id)
        new_email = result["user_email"] or (net_id + "@cornell.edu")
        new_year = result["user_year"] or "Freshman"
        new_description = result["user_description"] or " "
        courses = result["profile_courses"] or " "
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
        if '@' not in new_email:
            flash('A valid email is required.')
            return redirect("/profile/"+str(net_id))
        if not (new_year in ["Freshman","Sophomore","Junior","Senior","Graduate",
                            "Post-graduate"]):
            flash('A valid year is required')
            return redirect("/profile/"+str(net_id))
        Student.update_student(
            net_id, email=new_email, name=None, major=user.major,
            year=new_year, resume=filename, description=new_description,
            favorited_projects=None,
            availability=availability, courses=courses
        )
    else:
        if " " not in result.get('name', None).strip():
            flash('A valid name is required')
            return redirect("/profile/"+str(net_id))
        if '@' not in result.get('email', None):
            flash('A valid email is required')
            return redirect("/profile/"+str(net_id))
        Professor.update_professor(
            net_id,
            name=result.get('name', None),
            email=result.get('user_email', None),
            website=result.get('website', None),
            office=result.get('office_loc', None)
        )
    return redirect("/profile/" + net_id, code=302)


def current_semester(date):
    semester = None
    if date.month == 1:
        semester = "Winter" if date.day < 21 else "Spring"
    elif date.month < 5:
        semester = "Spring"
    elif date.month == 5:
        semester = "Spring" if date.day < 26 else "Summer"
    elif date.month < 8:
        semester = "Summer"
    elif date.month == 8:
        semester = "Summer" if date.day < 21 else "Fall"
    elif date.month < 12:
        semester = "Fall"
    elif date.month == 12:
        semester = "Fall" if date.day < 26 else "Winter"
    return semester


def semester_options(lookahead, curr_sem, year, options):
    if lookahead == 0:
        return options
    else:
        lookahead -= 1
        semesters = ["Spring", "Summer", "Fall", "Winter"]
        next_sem = semesters[(semesters.index(curr_sem) + 1) % 4]
        year = year + 1 if next_sem == "Spring" else year
        options.append(next_sem + " " + str(year))
        return semester_options(lookahead, next_sem, year, options)


@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def createpost():
    if current_user.is_student:
        return redirect('/')

    date = datetime.date.today()
    curr_sem = current_semester(date)
    options = semester_options(
        7, curr_sem, date.year, [curr_sem + " " + str(date.year)])

    if request.method == 'POST':
        result = request.form
        if (result.get("post_title") == ""):
            flash('Title Field is required.')
            return redirect("/posts/create")
        if result.get("post_description") == "":
            flash('Project Description is required')
            return redirect("/posts/create")
        if result.get('tags') == "":
            flash('Project Topics/Tags are required')
            return redirect("/posts/create")

        month = None
        day = None
        year = None
        if int(result['stale-days']) == -1:
            year = 2200
            day = 1
            month = 1
        else:
            stale_date = options[int(result['stale-days'])]
            semester = stale_date[:stale_date.find(" ")]
            year = int(stale_date[stale_date.find(" ") + 1:])

            if semester == "Fall":
                month = 12
                day = 25
            elif semester == "Winter":
                month = 1
                day = 20
            elif semester == "Spring":
                month = 5
                day = 25
            elif semester == "Summer":
                month = 8
                day = 20

        Post.create_post(
            title=result["post_title"].strip(),
            description=result["post_description"].strip(),
            professor_id=current_user.net_id,
            tags=result['tags'].lower().strip().split(','),
            stale_date=datetime.date(year=year, day=day, month=month),
            contact_email=result['post_professor_email'].strip(),
            project_link=result['project-link'].strip(),
            required_courses=result['courses'].lower().strip().split(','),
        )
        return redirect("/posts", code=301)
    else:
        return render_template(
            'createpost.html',
            base_url=BASE_URL,
            title='Submit Research Listing',
            all_tags=TAGS,
            all_courses=COURSES,
            post=Post.empty,
            options=options
        )


@app.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def showpost(post_id):
    post = Post.get_post_by_id(post_id)
    if not post or not post.is_active:
        return redirect('/')

    post = post.serialize
    post['professor_name'] = Professor.get_professor_by_netid(
        post['professor_id']).name
    print(post['courses'])

    return render_template(
        'full_post.html',
        base_url=BASE_URL,
        post=post
    )


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    post = Post.get_post_by_id(post_id)
    if not post:
        return redirect('/')

    date = datetime.date.today()
    curr_sem = current_semester(date)
    options = semester_options(
        7, curr_sem, date.year, [curr_sem + " " + str(date.year)])

    if request.method == 'POST':
        result = request.form
        is_active = bool(request.form.getlist('post-activate'))

        month = None
        day = None
        year = None
        if int(result['stale-days']) == -1:
            year = 2200
            day = 1
            month = 1
        else:
            stale_date = options[int(result['stale-days'])]
            semester = stale_date[:stale_date.find(" ")]
            year = int(stale_date[stale_date.find(" ") + 1:])

            if semester == "Fall":
                month = 12
                day = 25
            elif semester == "Winter":
                month = 1
                day = 20
            elif semester == "Spring":
                month = 5
                day = 25
            elif semester == "Summer":
                month = 8
                day = 20
        if (result.get("post_title") == ""):
            flash('Title Field is required.')
            return redirect("/posts/"+str(post_id)+"/edit")
        if result.get("post_description") == "":
            flash('Project Description is required')
            return redirect("/posts/"+str(post_id)+"/edit")
        if result.get('tags') == "":
            flash('Project Topics/Tags are required')
            return redirect("/posts/"+str(post_id)+"/edit")

        Post.update_post(
            post_id,
            is_active=is_active,
            description=result['post_description'].strip(),
            tags=result['tags'].split(','),
            required_courses=result['courses'],
            title=result['post_title'].strip(),
            contact_email=result['post_professor_email'].strip(),
            project_link=result['project-link'].strip(),
            stale_date=datetime.date(year=year, day=day, month=month)
        )
        return redirect('/posts/%s' % post_id)
    else:
        post = post.serialize
        post['tags'] = ",".join(post['tags'])
        post['courses'] = ",".join(post['courses'])
        return render_template(
            'createpost.html',
            base_url=BASE_URL,
            id='Sign In',
            all_tags=TAGS,
            all_courses=COURSES,
            post=post,
            options=options
        )


@app.errorhandler(413)
def file_too_large(e):
    flash('Resume File Size Exceeds Limit')
    return redirect("/profile/" + current_user.net_id, code=302)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorpages/404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('errorpages/403.html'), 403


@app.errorhandler(500)
def internal_error(e):
    return render_template('errorpages/500.html'), 500
