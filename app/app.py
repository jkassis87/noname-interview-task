from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# SQLite database connection
DATABASE = 'chinook.db'
def connect_db():
    return sqlite3.connect(DATABASE)

# route for index page
@app.route('/')
def index():
    return "Welcome to the Chinook Database API"

# route for tracks list
@app.route('/tracks')
def get_tracks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks")
    tracks = cursor.fetchall()
    conn.close()
    return render_template('tracks.html', tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)