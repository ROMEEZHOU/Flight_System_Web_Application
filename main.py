from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app=Flask(__name__,template_folder='template')


#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3307,
                       user='root',
                       password='',
                       db='DB_Project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello():
    return render_template('index.html',posts='')

@app.route('/SearchFlight1',methods=['GET', 'POST'])
def SearchFlight1():
    airline = request.form['airline']
    cursor=conn.cursor()
    query = 'SELECT flight_num FROM flight WHERE airline_name = %s'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['flight_num'])
    cursor.close()

    return render_template('index.html',posts=data1)



"""
#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')
"""

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug=True)
