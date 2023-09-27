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


# route to get all tracks
@app.route('/api/tracks/all', methods=['GET'])
def get_tracks():
    conn = connect_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks")
    tracks = cursor.fetchall()
    conn.close()
    return jsonify(tracks)

@app.route('/api/tracks/search')
def search_tracks():
    query = request.args.get('query', '')

    if not query:
        return jsonify({"error": "Please provide a search query"}), 400

    conn = connect_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks WHERE Name LIKE ?", ('%' + query + '%',))
    tracks = cursor.fetchall()
    conn.close()

    return jsonify(tracks)

# Read a specific track (GET endpoint)
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

# Create a new track (POST endpoint)
@app.route('/api/tracks', methods=['POST'])
def create_track():
    data = request.json
    if not data or 'Name' not in data or 'AlbumId' not in data or 'MediaTypeId' not in data:
        return jsonify({"error": "Invalid data"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tracks (Name, AlbumId, MediaTypeId) VALUES (?, ?, ?)",
                   (data['Name'], data['AlbumId'], data['MediaTypeId']))
    conn.commit()
    conn.close()

    return jsonify({"message": "Track created successfully"}), 201

# Update a track (PUT Endpoint)
@app.route('/api/tracks/<int:track_id>', methods=['PUT'])
def update_track(track_id):
    data = request.json
    if not data or ('Name' not in data and 'AlbumId' not in data and 'MediaTypeId' not in data):
        return jsonify({"error": "Invalid data"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks WHERE TrackId = ?", (track_id,))
    track = cursor.fetchone()
    if track is None:
        conn.close()
        return jsonify({"error": "Track not found"}), 404

    update_query = "UPDATE tracks SET "
    update_data = []
    if 'Name' in data:
        update_query += "Name = ?, "
        update_data.append(data['Name'])
    if 'AlbumId' in data:
        update_query += "AlbumId = ?, "
        update_data.append(data['AlbumId'])
    if 'MediaTypeId' in data:
        update_query += "MediaTypeId = ?, "
        update_data.append(data['MediaTypeId'])

    update_query = update_query.rstrip(', ')
    update_query += " WHERE TrackId = ?"
    update_data.append(track_id)

    cursor.execute(update_query, tuple(update_data))
    conn.commit()
    conn.close()

    return jsonify({"message": "Track updated successfully"})

# Delete a track (DELETE endpoint)
@app.route('/api/tracks/<int:track_id>', methods=['DELETE'])
def delete_track(track_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks WHERE TrackId = ?", (track_id,))
    track = cursor.fetchone()
    if track is None:
        conn.close()
        return jsonify({"error": "Track not found"}), 404

    cursor.execute("DELETE FROM tracks WHERE TrackId = ?", (track_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Track deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)