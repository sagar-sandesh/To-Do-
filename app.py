from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from nlp_utils import analyze_task
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Task

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    content = StringField('Task', validators=[DataRequired()])
    due_date = DateField('Due Date', default=datetime.date.today)
    priority = StringField('Priority (e.g., High, Medium, Low)')
    category = StringField('Category (e.g., Work, Home)')
    submit = SubmitField('Add/Update Task')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = TaskForm()
    if form.validate_on_submit():
        # Analyze task content for priority/category suggestion
        priority_suggestion, category_suggestion = analyze_task(form.content.data)
        # Override only if user did not enter
        priority = form.priority.data if form.priority.data else priority_suggestion
        category = form.category.data if form.category.data else category_suggestion

        task = Task(content=form.content.data,
                    due_date=form.due_date.data,
                    priority=priority,
                    category=category,
                    user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('index'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    return render_template('index.html', form=form, tasks=tasks)

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('index'))
    task.completed = True
    db.session.commit()
    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
