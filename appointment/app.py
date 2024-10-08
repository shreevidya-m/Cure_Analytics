from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', doctors=doctors)


APPOINTMENTS_DB = 'appointments.db'
DOCTORS_DB = 'doctors.db'

def create_appointments_table():
    conn = sqlite3.connect(APPOINTMENTS_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_name TEXT,
                 doctor_id INTEGER,
                 appointment_date TEXT)''')
    conn.commit()
    conn.close()

def create_doctors_table():
    conn = sqlite3.connect(DOCTORS_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 specialty TEXT)''')
    conn.commit()
    conn.close()

def add_sample_doctors():

    doctors = [
        ("Dr. John Doe", "Cardiology"),
        ("Dr. Jane Smith", "Dermatology"),
        ("Dr. Michael Johnson", "Orthopedics"),
        ("Dr. Sarah Thompson", "Pediatrics"),
        ("Dr. Robert Davis", "Neurology")
    ]

    conn = sqlite3.connect(DOCTORS_DB)
    c = conn.cursor()

    for doctor in doctors:
        name, specialty = doctor
        c.execute("SELECT * FROM doctors WHERE name = ?", (name,))
        existing_doctor = c.fetchone()
        if existing_doctor:
            continue  # Skip insertion if the doctor already exists
        c.execute("INSERT INTO doctors (name, specialty) VALUES (?, ?)", doctor)

    conn.commit()
    conn.close()

def get_doctors():
    conn = sqlite3.connect(DOCTORS_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM doctors")
    doctors = c.fetchall()
    conn.close()
    return doctors

create_appointments_table()
create_doctors_table()
add_sample_doctors()

@app.route('/doctors')
def doctors():
    doctors = get_doctors()
    return render_template('doctors.html', doctors=doctors)

@app.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
def book_appointment_route(doctor_id):
    def get_appointment_times():
        appointment_times = []
        start_time = datetime.datetime.strptime('10:00 AM', '%I:%M %p')
        end_time = datetime.datetime.strptime('5:00 PM', '%I:%M %p')
        time_interval = datetime.timedelta(hours=1)

        current_time = start_time
        while current_time <= end_time:
            appointment_times.append(current_time.strftime('%I:%M %p'))
            current_time += time_interval

        return appointment_times
    
    if request.method == 'GET':
        doctor = get_doctor(doctor_id)
        if doctor:
            appointment_times = get_appointment_times()
            return render_template('book_appointment.html', doctor=doctor, appointment_times=appointment_times)
        else:
            return "Doctor not found."
    elif request.method == 'POST':
        name = request.form['name']
        time = request.form['time']

        # Check if the selected time is already booked
        if is_time_slot_booked(doctor_id, time):
            return "The selected time is already booked. Please choose another time."

        # Insert the appointment into the database
        create_appointment(doctor_id, name, time)

        # Fetch the newly created appointment details
        appointment = (None, name, doctor_id, time)
        appointment_id = get_last_appointment_id()
        return redirect(url_for('appointment_confirmation', appointment_id=appointment_id))




def get_doctors():
    conn = sqlite3.connect(DOCTORS_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM doctors")
    doctors = c.fetchall()
    conn.close()
    return doctors

def get_doctor(doctor_id):
    conn = sqlite3.connect(DOCTORS_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    doctor = c.fetchone()
    conn.close()
    return doctor

def is_time_slot_booked(doctor_id, time):
    conn = sqlite3.connect(APPOINTMENTS_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM appointments WHERE doctor_id = ? AND appointment_date = ?", (doctor_id, time))
    appointment = c.fetchone()
    conn.close()
    return appointment is not None

def create_appointment(doctor_id, name, time):
    conn = sqlite3.connect(APPOINTMENTS_DB)
    c = conn.cursor()
    c.execute("INSERT INTO appointments (doctor_id, patient_name, appointment_date) VALUES (?, ?, ?)",
              (doctor_id, name, time))
    conn.commit()
    conn.close()
    print("Appointment created:", doctor_id, name, time)


def get_last_appointment_id():
    conn = sqlite3.connect(APPOINTMENTS_DB)
    c = conn.cursor()
    c.execute("SELECT id FROM appointments ORDER BY id DESC LIMIT 1")
    last_row_id = c.fetchone()
    conn.close()

    if last_row_id:
        return last_row_id[0]
    else:
        return None


@app.route('/appointment-confirmation/<int:appointment_id>')
def appointment_confirmation(appointment_id):
    appointment = get_appointment(appointment_id)
    if appointment:
        doctor_id = appointment[2]
        doctor = get_doctor(doctor_id)
        return render_template('appointment_confirmation.html', appointment=appointment, doctor=doctor)
    else:
        return f"Appointment not found. Appointment ID: {appointment_id}"




def get_appointment(appointment_id):
    conn = sqlite3.connect(APPOINTMENTS_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    appointment = c.fetchone()
    conn.close()
    return appointment if appointment else None

