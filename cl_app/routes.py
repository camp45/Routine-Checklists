from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse

from cl_app import app, db
from cl_app.forms import LoginForm, RegistrationForm, ItemForm, CheckListForm
from cl_app.models import User, CheckList, ListItem

@app.route('/')
@app.route('/index')
def index():
    checklists = CheckList.query.order_by(CheckList.creation_date.desc()).limit(10)
    return render_template('index.html',
                            title='Home Page',
                            checklists=checklists)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/new', methods=['GET', 'POST'])
@login_required
def create_new_checklist():
    form = CheckListForm()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit() and not CheckList.query.filter_by(title=form.title.data).first():
        list = CheckList(title=form.title.data, author=user)
        db.session.add(list)
        items = [ListItem(title=item.title.data, checklist=list) for item in form.item_list]
        db.session.add_all(items)
        db.session.commit()
        flash(f'Checklist "{list.title}" Created')
        return redirect(url_for('index'))
    return render_template('create_new_checklist.html',
                            title='New Check List',
                            form=form)


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
        flash(f'Welcome {user.username}')
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
        flash('Congrats, you are now a registerd user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    checklists = user.checklists.order_by(CheckList.creation_date.desc()).limit(10).all()
    return render_template('user.html', user=user, checklists=checklists)
