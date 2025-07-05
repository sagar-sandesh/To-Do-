# 📝 NLP-Enhanced To-Do List Web App

A clean and modern **Flask-based To-Do List Application** that allows users to register, log in, and manage their personal tasks. It leverages **Natural Language Processing (NLP)** using spaCy to intelligently suggest **priority** and **category** for each task.

---

## 🚀 Features

- 🔐 User Authentication (Register/Login/Logout)
- 🧠 NLP-Powered Task Suggestion:
  - Automatically predicts **priority** (High/Medium/Low)
  - Automatically classifies **category** (Work/Home/Study/etc.)
- ✅ Add, Complete, and Delete Tasks
- 🗓️ Assign Due Dates
- 🌓 Dark Mode Toggle
- 🎨 Beautiful Bootstrap 5 UI

---

## 🛠️ Tech Stack

| Layer        | Technology               |
|--------------|---------------------------|
| Backend      | Flask, Flask-WTF, Flask-Login, SQLAlchemy |
| NLP Engine   | spaCy (`en_core_web_sm`) |
| Frontend     | HTML + Bootstrap 5       |
| Database     | SQLite                    |

---

## 📁 Project Structure
project/
│
- ├── app.py # Main Flask app and routes
- ├── models.py # User and Task models
- ├── forms.py # Registration, Login, and Task forms
- ├── extensions.py # SQLAlchemy & Login manager instances
- ├── nlp_utils.py # NLP-based task analyzer
- ├── requirements.txt # Required dependencies
- ├── templates/ # Jinja2 HTML templates
- │ ├── base.html
- │ ├── index.html
- │ ├── login.html
- │ └── register.html
- └── static/ # (Optional) Static assets like CSS or JS


---

## 🧠 NLP Task Analyzer

`nlp_utils.py` uses spaCy to determine task **priority** and **category** based on keywords:
`
```python
import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_task(task_text):
    doc = nlp(task_text.lower())

    priority = 'Medium'
    category = 'General'

    high_priority_keywords = ['urgent', 'asap', 'immediately', 'important', 'high priority']
    low_priority_keywords = ['whenever', 'optional', 'low priority']

    for token in doc:
        if token.text in high_priority_keywords:
            priority = 'High'
        elif token.text in low_priority_keywords:
            priority = 'Low'

    if 'work' in task_text:
        category = 'Work'
    elif 'home' in task_text or 'clean' in task_text or 'chore' in task_text:
        category = 'Home'
    elif 'study' in task_text or 'read' in task_text or 'learn' in task_text:
        category = 'Study'

    return priority, category

```
## 🔐 Database Models
## 👤 User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
✅ Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(50), default='Medium')
    category = db.Column(db.String(100), default='General')
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  ---
## 🧾 requirements.txt
Flask
Flask-WTF
Flask-SQLAlchemy
Flask-Login
email-validator
spacy
werkzeug

---
## 📦 How to Run the App
### Clone the repo:
```bash
git clone https://github.com/yourusername/flask-nlp-todo.git
cd flask-nlp-todo
```

Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt
python -m spacy download en_core_web_sm

Run the app:
python app.py

Visit: http://localhost:5000

🎨 UI Screens (Templates)

| Template        | Description                              |
| --------------- | ---------------------------------------- |
| `base.html`     | Master layout, navbar, footer, dark mode |
| `index.html`    | Main dashboard for adding/managing tasks |
| `login.html`    | Login form                               |
| `register.html` | Registration form                        |

👤 Author
Sagar Sandesh Oli
📧 sagarsandesh45@gmail.com
📜 License
This project is open-source and free to use under the MIT License.
