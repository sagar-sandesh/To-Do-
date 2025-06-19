# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, DateField, PasswordField
# from wtforms.validators import DataRequired, Length, Email, EqualTo
# import datetime
#
# class RegistrationForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')
#
# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')
#
# class TaskForm(FlaskForm):
#     content = StringField('Task', validators=[DataRequired()])
#     due_date = DateField('Due Date', default=datetime.date.today)
#     priority = StringField('Priority (e.g., High, Medium, Low)')
#     category = StringField('Category (e.g., Work, Home)')
#     submit = SubmitField('Add/Update Task')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
