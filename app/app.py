from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLite database connection
DATABASE = 'chinook.db'

def connect_db():
    return sqlite3.connect(DATABASE)

# Helper function to convert database rows to dictionaries
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# App route for index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tracks')
def get_tracks_page():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks")
    tracks = cursor.fetchall()
    conn.close()
    return render_template('tracks.html', tracks=tracks)

# API routes for tracks
@app.route('/api/tracks', methods=['GET'])
def get_tracks():
    conn = connect_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks")
    tracks = cursor.fetchall()
    conn.close()
    return jsonify(tracks)

@app.route('/api/tracks/<int:track_id>', methods=['GET'])
def get_track(track_id):
    conn = connect_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks WHERE TrackId = ?", (track_id,))
    track = cursor.fetchone()
    conn.close()
    if track is None:
        return jsonify({"error": "Track not found"}), 404
    return jsonify(track)

if __name__ == '__main__':
    app.run(debug=True)