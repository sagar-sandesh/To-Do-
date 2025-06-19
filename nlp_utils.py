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
