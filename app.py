from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        group_members TEXT,
        school_name TEXT,
        project_title TEXT,
        project_theme TEXT,
        marks INTEGER,
        comments TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        data = (
            request.form['project_name'],
            request.form['group_members'],
            request.form['school_name'],
            request.form['project_title'],
            request.form['project_theme']
        )
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO submissions (project_name, group_members, school_name, project_title, project_theme) VALUES (?, ?, ?, ?, ?)', data)
        conn.commit()
        conn.close()
        return "Submitted Successfully!"
    return render_template('student.html')

@app.route('/judge', methods=['GET', 'POST'])
def judge():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        submission_id = request.form['id']
        marks = request.form['marks']
        comments = request.form['comments']
        c.execute('UPDATE submissions SET marks=?, comments=? WHERE id=?', (marks, comments, submission_id))
        conn.commit()
    c.execute('SELECT * FROM submissions')
    submissions = c.fetchall()
    conn.close()
    return render_template('judge.html', submissions=submissions)

if __name__ == '__main__':
app.run(host="0.0.0.0", port=10000)

