from flask import Flask, render_template, request
import sqlite3
from services.weather_service import get_weather
from services.ai_service import generate_itinerary
from services.pdf_service import export_itinerary_pdf

app = Flask(__name__)

# --- Database setup ---
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

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    ai_itinerary = None
    if request.method == 'POST':
        city = request.form['city']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Fetch weather
        weather = get_weather(city)

        # Save trip
        with sqlite3.connect('db.sqlite3') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO itineraries (city, start_date, end_date) VALUES (?,?,?)",
                      (city, start_date, end_date))
            conn.commit()

        # AI itinerary
        ai_itinerary = generate_itinerary(city, start_date, end_date, weather)

    return render_template('index.html', weather=weather, ai_itinerary=ai_itinerary)

@app.route('/itineraries')
def itineraries():
    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        c.execute("SELECT id, city, start_date, end_date FROM itineraries")
        trips = c.fetchall()
    return render_template('itineraries.html', itineraries=trips)

@app.route('/export/<int:trip_id>')
def export(trip_id):
    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        c.execute("SELECT city, start_date, end_date FROM itineraries WHERE id=?", (trip_id,))
        trip = c.fetchone()
    if trip:
        pdf_path = export_itinerary_pdf(trip[0], trip[1], trip[2])
        return f"✅ PDF created at: {pdf_path}"
    return "Trip not found", 404

if __name__ == '__main__':
    app.run(debug=True)