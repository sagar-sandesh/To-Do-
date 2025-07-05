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
To-DO-/

- ├── app.py
- ├── models.py 
- ├── forms.py 
- ├── extensions.py 
- ├── nlp_utils.py 
- ├── requirements.txt
- ├── instance/
- │ ├── todo.db
- ├── templates/ 
- │ ├── base.html
- │ ├── index.html
- │ ├── login.html
- │ └── register.html
- ├── static/ 
- │  ├── js /
- │    ├── style.css

---

## 🧠 NLP Task Analyzer

nlp_utils.py uses spaCy to determine task **priority** and **category** based on keywords:

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
### 👤 User
```bash
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
```
### ✅ Task
```bash
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(50), default='Medium')
    category = db.Column(db.String(100), default='General')
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```
  ---
## 🧾 requirements.txt
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Login
- email-validator
- spacy
- werkzeug

---
## 📦 How to Run the App
### 1.Clone the repo:
```bash
git clone https://github.com/yourusername/flask-nlp-todo.git
cd flask-nlp-todo
```

### 2.Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3.Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
### 4.Run the app:
```bash
python app.py
```

### 5.Visit: http://localhost:5000
---
## 🎨 UI Screens (Templates)

| Template        | Description                              |
| --------------- | ---------------------------------------- |
| `base.html`     | Master layout, navbar, footer, dark mode |
| `index.html`    | Main dashboard for adding/managing tasks |
| `login.html`    | Login form                               |
| `register.html` | Registration form                        |

## 👤 Author
- Mr Sagar Sandesh Oli
- 📧 olisagarsandesh@gmail.com
- 📍 Kirstintie, Espoo, Finland
- 📞 +358402457337

## 📜 License
This project is open-source and free to use under the MIT License.
