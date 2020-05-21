from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from cl_app import app
from cl_app.forms import LoginForm
from cl_app.models import User

@app.route('/')
@app.route('/index')
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
    return render_template('index.html', check_lists=check_lists)


@app.route('/new')
def create_new_checklist():
    content = 'Make a new checklist here!'
    return render_template('create_new_checklist.html', content=content)


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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
