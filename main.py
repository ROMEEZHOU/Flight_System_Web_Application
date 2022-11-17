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

@app.route('/SearchFlightStatus',methods=['GET','POST'])
def search_flight_status():
    pass




#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/CustomerLogin')
def customer_login():
    return render_template('customer_login.html')

@app.route('/StaffLogin')
def staff_login():
    return render_template('staff_login.html')

@app.route('/CustomerRegister')
def customer_register():
    return render_template('customer_register.html')

@app.route('/StaffRegister')
def staff_register():
    return render_template('staff_register.html')

@app.route('/CustomerLoginAuth',methods=['GET', 'POST'])
def customer_login_auth():
    #grabs information from the forms
	email = request.form['email']
	password = request.form['password']

    #cursor used to send queries
	cursor = conn.cursor()

	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and customer_password = MD5(%s)'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		return redirect(url_for('customer_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customer_login.html', error=error)

@app.route('/StaffLoginAuth',methods=['GET', 'POST'])
def staff_login_auth():
    #grabs information from the forms
	username = request.form['username']
	user_password = request.form['password']

    #cursor used to send queries
	cursor = conn.cursor()

	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and user_password = MD5(%s)'
	cursor.execute(query, (username, user_password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('staff_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('staff_login.html', error=error)


@app.route('/customer_home',methods=['GET', 'POST'])
def customer_home():
    
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('customer_home.html', username=username, posts=data1)

@app.route('/staff_home',methods=['GET', 'POST'])
def staff_home():
    
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('staff_home.html', username=username, posts=data1)


@app.route('/CustomerRegisterAuth',methods=['GET', 'POST'])
def customer_register_auth():
    #grabs information from the forms
    email = request.form['email']
    name = request.form['name']
    customer_password = request.form['password']
    building_number=request.form['building_number']
    street=request.form['street']
    city=request.form['city']
    state=request.form['state']
    phone_number=request.form['phone_number']
    passport_number=request.form['passport_number']
    passport_expiration=request.form['passport_expiration']
    passport_country=request.form['passport_country']
    date_of_birth=request.form['date_of_birth']
    try:
        building_number=int(building_number)
        print(building_number)
        print(type(building_number))
    except:
        error = "Building number must be an integer"
        return render_template('customer_register.html', error = error)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This email is been used"
        return render_template('customer_register.html', error = error)
    if not isinstance(building_number, int):
        error = "Building number must be an integer"
        return render_template('customer_register.html', error = error)
        
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, name, customer_password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth))
        conn.commit()
        cursor.close()
        return render_template('login.html')

@app.route('/StaffRegisterAuth',methods=['GET', 'POST'])
def staff_register_auth():
    #grabs information from the forms
    username=request.form['username']
    user_password = request.form['user_password']
    first_name=request.form['first_name']
    last_name=request.form['last_name']
    date_of_birth=request.form['date_of_birth']
    airline=request.form['airline']
    phone_num=request.form['phone_num']
    email=request.form['email']

    phone_list=phone_num.split(',')
    email_list=email.split(',')


	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query1 = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query1, (username))
	#stores the results in a variable
    data1 = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    error = None

    query2='SELECT * FROM airline WHERE name = %s'
    cursor.execute(query1, (airline))
    data2 = cursor.fetchone()
    if not data2:
        error = 'This airline does not exist'
        return render_template('staff_register.html', error = error)

    if(data1):
		#If the previous query returns data, then user exists
        error = "This username is been already existed"
        return render_template('staff_register.html', error = error)

        
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s , %s, %s)'
        cursor.execute(ins, (username, user_password, first_name, last_name, date_of_birth, airline))
        for phone_n in phone_list:
            ins_phone = 'INSERT INTO staff_phone VALUES(%s, %s)'
            cursor.execute(ins,(username,phone_n))

        for e in email_list:
            ins_email='INSERT INTO staff_email VALUES(%s, %s)'
            cursor.execute(ins,(username,e))

        conn.commit()
        cursor.close()
        return render_template('login.html')

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug=True)
