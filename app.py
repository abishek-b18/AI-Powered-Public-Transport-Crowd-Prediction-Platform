from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "transport_secret_key"

# Load trained model
model = pickle.load(open("crowd_model.pkl", "rb"))

# Database connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create user table
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

# Home Page
@app.route('/')
def home():
    return render_template("index.html")

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (username,email,password) VALUES (?,?,?)",
            (username, email, password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template("register.html")

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:
            session['user'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"

    return render_template("login.html")

# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        "dashboard.html",
        username=session['user']
    )

# Prediction Page
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':

        vehicle = int(request.form['vehicle'])
        weather = int(request.form['weather'])
        holiday = int(request.form['holiday'])
        passenger_count = int(request.form['passenger_count'])
        occupancy = int(request.form['occupancy'])

        prediction = model.predict(
            [[vehicle,
              weather,
              holiday,
              passenger_count,
              occupancy]]
        )[0]

        labels = {
            0: "High Crowd",
            1: "Low Crowd",
            2: "Medium Crowd"
        }

        result = labels[prediction]

        return render_template(
            "prediction.html",
            prediction=result
        )

    return render_template(
        "prediction.html",
        prediction=None
    )

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)