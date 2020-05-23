from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from cl_app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit Registration')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please Chose a Different Username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please Use a Different Email Address')


class ItemForm(FlaskForm):
    title = StringField('List Item', validators=[DataRequired()])

class CheckListForm(FlaskForm):
    title = StringField('Checklist Title', validators=[DataRequired()])
    item_list = FieldList(FormField(ItemForm), min_entries=2)
    submit = SubmitField('Submit Registration')

