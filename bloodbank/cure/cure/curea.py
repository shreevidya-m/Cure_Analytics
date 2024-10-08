
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__, static_folder='static')

@app.route('/')
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

def create_user_table():
    conn=sqlite3.connect('curea.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ADDDONOR(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    blood_type TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    donation_date TEXT NOT NULL
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS BLOODTEST(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    location TEXT NOT NULL
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS EMERGENCY (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    blood_type TEXT NOT NULL,
                    location TEXT NOT NULL,
                    contact TEXT NOT NULL
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS AVAILABLITY (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    blood_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL
                )''')  
    conn.commit()
    conn.close()


@app.route('/bloodbank', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form.get("name")
        blood_type = request.form.get("blood_type")
        age = request.form.get("age")
        gender = request.form.get("gender")
        contact = request.form.get("contact")
        email = request.form.get("email")
        address = request.form.get("address")
        donation_date = request.form.get("donation_date")
        
        conn = sqlite3.connect('curea.db')
        cursor= conn.cursor()
        cursor.execute('''INSERT INTO  ADDDONOR
                    (name, blood_type, age, gender, contact, email, address, donation_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                (name, blood_type, age, gender, contact, email, address, donation_date))
        conn.commit()
        conn.close()
        
        return "Donor details added successfully!"
    else:
        return render_template('bloodbank.html')
        


@app.route("/donorsearch", methods=['GET','POST'])
def search():
    if request.method == 'POST':
        blood_type = request.form.get("blood_type")
        if blood_type != blood_type:
            return render_template('donor_search.html', error='Blood not available')
        
        conn = sqlite3.connect('curea.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ADDDONOR WHERE blood_type = ?", (blood_type,))
        donor=cursor.fetchall()

        conn.commit()
        conn.close()
        return donor
    else:
        return render_template('donor_search.html')
        

    # Perform the search logic and retrieve matching donors from the database
    # Example: query the database based on the selected blood type

    # Mock search results for demonstration



@app.route("/schedule")
def index2():
    return render_template("schedule.html")

@app.route("/schedule", methods=["POST"])
def schedule():
    name = request.form.get("name")
    date = request.form.get("date")
    time = request.form.get("time")
    appointment_type= request.form.get("appointment_type")
    # Process the appointment data as needed
    # Example: store in a database, perform validations, etc.

    return "Appointment scheduled successfully!"

def insert_blood_availability(blood_data):
    conn = sqlite3.connect('curea.db')
    cursor= conn.cursor()
    try:
        cursor.execute('''INSERT INTO AVAILABLITY
                        (blood_type, quantity) 
                        VALUES (?, ?)''', blood_data)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Error occurred:",e)
        conn.rollback()
        return False
    finally:
        conn.close()

@app.route("/availablity", methods=["GET", "POST"])
def blood_availability():
    if request.method == "POST":
        blood_type = request.form.get("blood_type")
        quantity = request.form.get("quantity")

        blood_data = (blood_type, quantity)

        if insert_blood_availability(blood_data):
            return "Blood availability data submitted successfully!"
        else:
            return "Error occurred while submitting blood availability data."

    return render_template("availablity.html")



def insert_emergency_request(request_data):
    conn = sqlite3.connect('curea.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO EMERGENCY
                        (name, blood_type, contact, location) 
                        VALUES (?, ?, ?, ?)''', request_data)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Error occurred:", e)
        conn.rollback()
        return False
    finally:
        conn.close()

@app.route("/emergency", methods=["GET", "POST"])
def emergency():
    if request.method == "POST":
        name = request.form.get("name")
        blood_type = request.form.get("blood_type")
        contact = request.form.get("contact")
        location = request.form.get("location")

        request_data = (name, blood_type, contact, location)

        if insert_emergency_request(request_data):
            return "Emergency request submitted successfully!"
        else:
            return "Error occurred while submitting emergency request."

    return render_template("emergency.html")

        
@app.route("/bloodtest",methods=['GET', 'POST'])
def bloodtest():
    if request.method == "POST":
        test_name = request.form.get("test_name")
        date = request.form.get("date")
        location = request.form.get("location")

        
        conn = sqlite3.connect('curea.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO BLOODTEST
                        (test_name, date, location) 
                        VALUES (?, ?, ?)''', (test_name, date, location))
       
        conn.commit()
        conn.close()
        return "Blood test details added successfully"
    else:
        return render_template('bloodtest.html')

if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)


