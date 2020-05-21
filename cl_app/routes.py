from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse

from cl_app import app, db
from cl_app.forms import LoginForm, RegistrationForm
from cl_app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    check_lists = [{'author': {'username': 'Brad'},
                    'title': 'Monday Chores',
                    'items': ['Take out trash', 'Test the app']
                    },
                    {
                    'author': {'username': 'Frank'},
                    'title': 'Pre Takeoff Checklist',
                    'items': ['Doors','Brakes', 'Flight Controls',
                              'Flight Instruments']}]
    return render_template('index.html',
                            title='Home Page',
                            check_lists=check_lists)


@app.route('/new')
def create_new_checklist():
    content = 'Make a new checklist here!'
    return render_template('create_new_checklist.html',
                            title='New Check List',
                            content=content)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {user.username}.')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are not a registerd user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
