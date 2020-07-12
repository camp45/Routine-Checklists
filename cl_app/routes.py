from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse

from cl_app import app, db
from cl_app.forms import LoginForm, RegistrationForm, CreateItemForm, CheckListForm
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
        db.session.commit()
        flash(f'Checklist "{list.title}" Created')
        return redirect(url_for('edit_checklist', checklist_id=list.id))
    return render_template('create_new_checklist.html',
                            title='New Check List',
                            form=form)


@app.route('/checklist/<int:checklist_id>')
def checklist(checklist_id):
    checklist = CheckList.query.get(checklist_id)
    if checklist:
        return render_template('checklist.html', checklist=checklist)
    else:
        flash('Checklist not found')
        return redirect(url_for('index'))


@app.route('/checklist/<int:checklist_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_checklist(checklist_id):
    checklist = CheckList.query.get(checklist_id)
    form = CreateItemForm(checklist_id=checklist.id)
    if checklist:
        if checklist.author.username == current_user.username:
            if request.method == 'GET':
                item_forms = []
                for item in checklist.listitems.all():
                    temp_form = CreateItemForm()
                    temp_form.process(obj=item)
                    item_forms.append(temp_form)
                return render_template('edit_checklist.html', checklist=checklist, form=form, item_forms=item_forms)
            if request.method == 'POST' and form.validate_on_submit() and request.args.get('action') == 'add':
                list_item = ListItem(title=form.item_text.data, checklist_id=form.checklist_id.data)
                db.session.add(list_item)
                db.session.commit()
                flash(f"Item '{form.item_text.data}' added to {checklist.title}.")
                form = CreateItemForm(checklist_id=checklist.id)
                return render_template('edit_checklist.html', checklist=checklist, form=form)
            elif request.method == 'POST' and request.args.get('action') == 'delete':
                pass
            return render_template('edit_checklist.html', checklist=checklist, form=form)
        else:
            flash("You don't own this checklist, and therefore can't edit it.")
            return redirect(url_for('index'))
    else:
        flash('Checklist not found')
        return redirect(url_for('index'))

@app.route('/listitem/delete', methods=['POST'])
@login_required
def edit_list_item():
    form = CreateItemForm()
    if form.validate_on_submit():
        item = ListItem.query.get(form.id.data)
        try:
            db.session.delete(item)
            db.session.commit()
            flash(f"Item '{form.title.data}' deleted")
            return redirect(url_for('edit_checklist', checklist_id=item.checklist_id))
        except:
            pass
    flash('Error in form')
    return redirect(url_for('edit_checklist', checklist_id=item.checklist_id))



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
