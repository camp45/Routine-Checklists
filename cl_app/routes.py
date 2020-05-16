from flask import render_template, flash, redirect, url_for

from cl_app import app
from cl_app.forms import LoginForm

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
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'User {form.username.data} logged in!')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
