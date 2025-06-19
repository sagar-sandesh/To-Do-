from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm
from models import db, User, Task
from nlp_utils import extract_priority
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db.init_app(app)
bcrypt = Bcrypt(app)

# ---------------- User Session ----------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# ---------------- Routes ----------------
@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', tasks=tasks)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registered Successfully!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash("Invalid credentials", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add-task', methods=['POST'])
@login_required
def add_task():
    task_text = request.form.get('task')
    priority = extract_priority(task_text)
    task = Task(description=task_text, priority=priority, user_id=session['user_id'])
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

# ---------------- REST API ----------------
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return jsonify([task.as_dict() for task in tasks])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
