from flask import Flask, render_template, request
from datetime import date
import pymysql
import pymysql.cursors

_configVars = {"cdmDBHost": "db.webapp", "cdmDBuser": "root", "cdmDBpwd": "NNYp9XM4zkDnZvn5", "cdmDB": "test", "cdmDBPort": 3306}
cur = pymysql.connect(host=_configVars["cdmDBHost"], user=_configVars["cdmDBuser"], password=_configVars["cdmDBpwd"], database=_configVars["cdmDB"], port= _configVars["cdmDBPort"], cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

#Function to calculate age from date of birth
def calculate_age(dob):
    birth_date = date.fromisoformat(dob)
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def create_table():
    try:
        with cur.cursor() as _cursor:
            _sqlStmt = "CREATE TABLE customers (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), email VARCHAR(255), phone VARCHAR(20),city VARCHAR(50), dob DATE, age INT)"
            _cursor.execute(_sqlStmt)
        cur.commit()
        cur.close()
    except:
        pass

#Define the index route
@app.route('/')
def index():
    return render_template('index.html')

#Define the submit route
@app.route('/submit', methods=['POST'])
def submit():
    #Get form data from request
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    city = request.form['city']
    dob = request.form['dob']
    age = calculate_age(dob)

    #Insert data into database
    with cur.cursor() as _cursor:
        _sqlStmt = "INSERT INTO customers (name, phone, email, city, dob, age) VALUES (%s, %s, %s, %s, %s, %s)"
        _cursor.execute(_sqlStmt, (name, phone, email, city, dob, age))

    cur.commit()

    with cur.cursor() as _cursor:
        _sqlStmt = "SELECT age FROM customers where name = %s and phone = %s and email = %s and city = %s and dob = %s"
        _cursor.execute(_sqlStmt, (name, phone, email, city, dob))
        user_age = _cursor.fetchall()
        user_age = [dict(row)["age"] for row in user_age][0]

    cur.commit()
    cur.close()

    return render_template('submit.html', name=name, age=user_age)

if __name__ == '__main__':
    create_table()
    app.run()
