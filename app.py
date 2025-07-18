from flask import Flask
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS itineraries
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      city TEXT,
                      start_date TEXT,
                      end_date TEXT,
                      notes TEXT)''')
        conn.commit()

init_db()

@app.route("/")
def home():
    return "Database initialized. Travel Planner is running!"

if __name__ == "__main__":
    app.run(debug=True)