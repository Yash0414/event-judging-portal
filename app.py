from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to something secure

# Judge credentials (you can later load from .env)
USERNAME = 'judge'
PASSWORD = 'event123'

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

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Student submission form
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

# Judge login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('judge'))
        else:
            return "<h3 style='color:red;'>Invalid credentials</h3><a href='/login'>Try again</a>"
    return '''
        <h2 style='text-align:center;'>Judge Login</h2>
        <form method="post" style="width:300px;margin:auto;">
            <input type="text" name="username" placeholder="Username" required><br><br>
            <input type="password" name="password" placeholder="Password" required><br><br>
            <input type="submit" value="Login">
        </form>
    '''

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Judge panel
@app.route('/judge', methods=['GET', 'POST'])
def judge():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

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
    app.run(host='0.0.0.0', port=10000)

