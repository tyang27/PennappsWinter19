from flask import Flask, render_template, url_for, request
from datetime import datetime
import os

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

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_data():
    wf='No input detected'
    if request.method == 'POST':
        print('POST')
        wf = request.form['waveform']
    return render_template('results.html', waveform = wf)

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        print('Checkin post')
        print(request.form)
    username = request.form['username']
    print(username)
    time = request.form['time'] if request.form['time'] != '' else datetime.now().strftime('%H:%M')
    return render_template('checkin.html',
        username=username,
        time=time)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        print('Checkout post')
        print(request.form)
    username = request.form['username']
    print(username)
    time = request.form['time'] if request.form['time'] != '' else datetime.now().strftime('%H:%M')
    return render_template('checkout.html',
        username=username,
        time=time)


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

@app.route('/')
def index():
    """Render home page."""
    return render_template('index.html', increments=INCREMENTS)

if __name__ == '__main__':
    app.run()
