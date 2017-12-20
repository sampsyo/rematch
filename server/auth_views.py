"""The views for standard username/password login to the application.
"""
from flask import render_template, flash, redirect, request
from server import app
from flask_login import login_user, logout_user, login_required

from .forms import LoginForm, RegistrationForm
from .utils import get_redirect_target
from .models import Student, Professor


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        app.logger.info('Registering: %s', form.is_student.data)
        if Student.get_student_by_netid(form.net_id.data) or \
           Professor.get_professor_by_netid(form.net_id.data):
                flash('A Profile has already been created with that Net ID')
                return redirect('/register')
        if form.is_student.data:
            Student.create_student(
                net_id=form.net_id.data, name=form.name.data,
                email=form.email.data, password=form.password.data)
        else:
            Professor.create_professor(
                net_id=form.net_id.data, name=form.name.data,
                email=form.email.data, password=form.password.data
            )
        flash('Thanks for registering!')
        return redirect('/login')
    return render_template('register.html', form=form)


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
                next_url = get_redirect_target()
                return redirect(next_url or app.config['BASE_URL'])
            else:
                flash('Username or Password Incorrect!')
                return redirect('/login')
    return render_template(
        'login.html',
        base_url=app.config['BASE_URL'],
        form=form
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(app.config['BASE_URL'])
