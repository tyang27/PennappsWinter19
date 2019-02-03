from flask import Flask, render_template, url_for, request, flash, Session
from datetime import datetime
import pandas as pd
import os

import algorithm as sch
from algorithm import Week, Day

UPLOADS = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
INCREMENTS = [
    '09:00', '09:15', '09:30', '09:45',
    '10:00', '10:15', '10:30', '10:45',
    '11:00', '11:15', '11:30', '11:45',
    '12:00', '12:15', '12:30', '12:45',
    '13:00', '13:15', '13:30', '13:45',
    '14:00', '14:15', '14:30', '14:45',
    '15:00', '15:15', '15:30', '15:45',
    '16:00', '16:15', '16:30', '16:45',
    '17:00'
    ]
SCHEDULE = []

# FLASK APP
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()

# BACKEND DATA
week = sch.Week()
patient_roster = pd.read_csv("data/patient_roster.csv")
patient_data = pd.read_csv("data/patient_data.csv")

# Construct an inflatable table from Week object
dayofweek_translate = {
        "Monday":2,
        "Tuesday":3,
        "Wednesday":4,
        "Thursday":5,
        "Friday":6
        }
def time_translate(military_time):
    return int((military_time - 900) / 100)

def build_week(week):
    SCHEDULE = []
    for dayofweek, day in week.days.items():
        for pat_time, pat_id in day.ppl.items():
            SCHEDULE.append((pat_id, time_translate(pat_time), dayofweek_translate[dayofweek]))
    return SCHEDULE

pat_cnt = 0
@app.route('/incoming', methods=['GET','POST'])
def incoming():
    """Handle scheduling for new user and re-render home page."""
    if request.method == 'POST':
        print('POST')
        print(request.form)
        if request.form['day'] == '':
            print('empty field')
            
        sch.schedule_appt(week, request.form['day'], pat_cnt, patient_roster)
        pat_cnt += 1

    return render_template('index.html', increments=INCREMENTS, time=SCHEDULE)

@app.route('/returning', methods=['GET','POST'])
def returning():
    """Handle scheduling for return user and re-render home page."""
    if request.method == 'POST':
        print('POST')
        print(request.form)

        if request.form['id'] == '' or request.form['day'] == '':
            print('empty field')
            return render_template('index.html', increments=INCREMENTS)

        SCHEDULE.append((int(request.form['id']), len(SCHEDULE), dayofweek_translate[request.form['day']]))
    return render_template('index.html', increments=INCREMENTS, time=SCHEDULE)

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    """Handle checkout form submission and re-render home page."""
    if request.method == 'POST':
        username = request.form['username']
        time = request.form['time'] if request.form['time'] != '' else datetime.now().strftime('%H:%M')
        print(request.form)
    return render_template('index.html', increments=INCREMENTS, time=SCHEDULE)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Handle checkout form submission and re-render home page."""
    if request.method == 'POST':
        username = request.form['username']
        time = request.form['time'] if request.form['time'] != '' else datetime.now().strftime('%H:%M')
        print(request.form)
    return render_template('index.html', increments=INCREMENTS, time=SCHEDULE)

@app.route('/')
def index():
    """Render home page."""
    # (day of week, start time, user id, probability))
    return render_template('index.html', increments=INCREMENTS, time=SCHEDULE)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    pat_cnt = 0
    app.run()
