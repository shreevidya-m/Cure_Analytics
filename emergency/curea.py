from flask import Flask, render_template, request,url_for,redirect,session,flash  
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

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/nearesthospital')
def nearesthospital():
    return render_template('nearesthospital.html')
    
@app.route('/ambulance')
def ambulance():
    return render_template('ambulance.html')



# Function to create the database table (if not exists)
def create_table():
    conn = sqlite3.connect('cure.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS c(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            mobile TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            consultation_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/doorstepdoctor', methods=['GET', 'POST'])
def doorstepdoctor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        mobile = request.form['mobile']
        address = request.form['address']
        pincode = request.form['pincode']
        consultation_type = request.form['consultation']
        
        conn = sqlite3.connect('cure.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consultations (name, age, gender, mobile, address, pincode, consultation_type) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, age, gender, mobile, address, pincode, consultation_type))
        conn.commit()
        conn.close()

        return render_template('bookeddsp.html', name=name, consultation_type=consultation_type)
    else:
        return render_template('doorstepdoctor.html')
@app.route('/bookeddsp')
def bookeddsp():
    name = request.args.get('name')
    consultation_type = request.args.get('consultation_type')
    return render_template('bookeddsp,html', name=name, consultation_type=consultation_type)
if __name__ == '__main__':
    create_table()
    app.run()


