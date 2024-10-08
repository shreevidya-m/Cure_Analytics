from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run()


