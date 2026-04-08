from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS plans
                 (id INTEGER PRIMARY KEY, subject TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    plan = []

    if request.method == 'POST':
        subjects = request.form['subjects'].split(',')
        exam_date = datetime.strptime(request.form['exam_date'], '%Y-%m-%d')
        today = datetime.today()

        days = (exam_date - today).days
        per_day = max(1, len(subjects) // max(1, days))

        current_date = today

        for subject in subjects:
            plan.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'subject': subject.strip()
            })
            current_date += timedelta(days=1)

    return render_template('index.html', plan=plan)

if __name__ == '__main__':
    app.run(debug=True, port=5000)