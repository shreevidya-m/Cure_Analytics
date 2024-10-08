from flask import Flask, render_template

app = Flask(__name__, static_folder='static')


@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/bank')
def bank():
    return render_template('bank.html')

@app.route('/about')
def about():
    return render_template('about.html')

patients = [
    {"id": 1, "name": "John Doe", "check_in": "09:00 AM", "check_out": "04:30 PM", "attendance": "present"},
    {"id": 2, "name": "Jane Smith", "check_in": "10:15 AM", "check_out": "02:45 PM", "attendance": "present"}
]

@app.route('/')
def attendance():
    return render_template('attendance.html', patients=patients)

 

if __name__ == '__main__':
    app.run()


