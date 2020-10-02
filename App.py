from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'devices_db'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM area_device')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        # reading form fields
        name = request.form['device-name']
        active = request.form['active']
        area_id = request.form['area']
        cur = mysql.connection.cursor()

        # inserting data into devices
        cur.execute("INSERT INTO devices (name, active) VALUES (%s,%s)", (name, active))
        mysql.connection.commit()
        device_id = cur.lastrowid

        # inserting data into areas
        cur.execute("INSERT INTO area_device (area_id, device_id) VALUES (%s,%s)", (area_id, device_id))
        mysql.connection.commit()

        # reading multiple checkbox data and inserting into sensor_device
        sensor_types = request.form.getlist("sensor")
        if len(sensor_types)!=0:
            for i in range(0, len(sensor_types)): 
                sensor_types[i] = (device_id, int(sensor_types[i]))
            cur.executemany("INSERT INTO sensor_device (device_id, sensor_id) VALUES (%s, %s)", (sensor_types))
            mysql.connection.commit()
        
        # shows message
        flash('Device Added successfully')
        return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
