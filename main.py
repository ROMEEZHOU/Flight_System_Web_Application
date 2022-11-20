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

###############################################################################
###############################################################################
########################## Main Home Page #####################################

@app.route('/')
def hello():
    return render_template('index.html',posts='')

@app.route('/SearchFlight1',methods=['GET', 'POST'])
def SearchFlight1():
    departure = request.form['departure']
    destination=request.form['destination']
    dept_date=request.form['dept_date']
    return_date=request.form['return_date']
    if 'round_trip' in request.form:
        if return_date!='':
            cursor=conn.cursor()
            query1='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
            cursor.execute(query1, (departure, destination, dept_date, departure, dept_date, destination, destination, dept_date, departure, dept_date, departure, destination))
            data1=cursor.fetchall()

            query2='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
            cursor.execute(query1, (destination, departure, return_date, destination, return_date, departure, departure, return_date, destination, return_date, destination, departure))
            data2=cursor.fetchall()
            cursor.close()

            return render_template('index.html',post1=data1,post2=data2)

        else:
            return render_template('index.html',error='Please select the return date')

    else:
        cursor=conn.cursor()
        query='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
        cursor.execute(query, (departure, destination, dept_date, departure, dept_date, destination, destination, dept_date, departure, dept_date, departure, destination))
        data=cursor.fetchall()
        cursor.close()
        return render_template('index.html',post1=data)

    '''
    cursor=conn.cursor()
    query = 'SELECT flight_num FROM flight WHERE airline_name = %s'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['flight_num'])
    cursor.close()

    return render_template('index.html',post1=data1)'''


@app.route('/SearchFlightStatus',methods=['GET','POST'])
def search_flight_status():
    airline= request.form['airline']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    arr_date=request.form['arr_date']

    if dept_date=='':
        if arr_date=='':
            return render_template('index.html',error='Please enter either departure date or arrival date')
        else:
            cursor=conn.cursor()
            query='SELECT * FROM flight WHERE airline_name= %s AND flight_num = %s AND arr_date= %s'
            cursor.execute(query, (airline, flight_num, arr_date))
            data=cursor.fetchall()
            cursor.close()
            return render_template('index.html',post3=data)
    else:
        if arr_date=='':
            cursor=conn.cursor()
            query='SELECT * FROM flight WHERE airline_name= %s AND flight_num = %s AND dept_date= %s'
            cursor.execute(query, (airline, flight_num, dept_date))
            data=cursor.fetchall()
            cursor.close()
            return render_template('index.html',post3=data)

        else:
            cursor=conn.cursor()
            query='SELECT * FROM flight WHERE airline_name= %s AND flight_num = %s AND dept_date= %s AND arr_date = %s'
            cursor.execute(query, (airline, flight_num, dept_date, arr_date))
            data=cursor.fetchall()
            cursor.close()
            return render_template('index.html',post3=data)


###############################################################################
###############################################################################
########################## Login And Register #################################


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

@app.route('/CustomerLoginAuth',methods=['GET', 'POST'])
def customer_login_auth():
    #grabs information from the forms
    email = request.form['email']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()

    #executes query
    query = 'SELECT name FROM customer WHERE email = %s and customer_password = %s'
    cursor.execute(query, (email, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        session['type']='customer'
        session['username'] = data['name']
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
    query = 'SELECT * FROM airline_staff WHERE username = %s and user_password = %s'
    cursor.execute(query, (username, user_password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['type'] = 'staff'
        session['username'] = username
        return redirect(url_for('staff_home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('staff_login.html', error=error)


###############################################################################
###############################################################################
########################## Customer Home Pages ################################


@app.route('/customer_home',methods=['GET', 'POST'])
def customer_home():
    if session.get('type')!='customer' or not session.get('username'):
        return redirect('/')
    username = session['username']
    return render_template('customer_home.html', username=username)

@app.route('/customer_search_flight',methods=['GET', 'POST'])
def customer_search_flight():
    departure = request.form['departure']
    destination=request.form['destination']
    dept_date=request.form['dept_date']
    return_date=request.form['return_date']
    if 'round_trip' in request.form:
        if return_date!='':
            cursor=conn.cursor()
            query1='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
            cursor.execute(query1, (departure, destination, dept_date, departure, dept_date, destination, destination, dept_date, departure, dept_date, departure, destination))
            data1=cursor.fetchall()

            query2='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
            cursor.execute(query1, (destination, departure, return_date, destination, return_date, departure, departure, return_date, destination, return_date, destination, departure))
            data2=cursor.fetchall()
            cursor.close()

            return render_template('customer_home.html',post1=data1,post2=data2)

        else:
            return render_template('customer_home.html',error='Please select the return date')

    else:
        cursor=conn.cursor()
        query='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
        cursor.execute(query, (departure, destination, dept_date, departure, dept_date, destination, destination, dept_date, departure, dept_date, departure, destination))
        data=cursor.fetchall()
        cursor.close()
        return render_template('customer_home.html',post1=data)


@app.route('/book_flight',methods=['GET', 'POST'])
def book_flight():
    if session.get('type')!='customer' or not session.get('username'):
        return redirect('/')
    username = session['username']
    airline=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    arr_date=request.form['arr_date']
    arr_time=request.form['arr_time']
    dept_airport=request.form['dept_airport']
    arr_airport=request.form['arr_airport']
    base_price=request.form['base_price']
    flight_status=request.form['flight_status']
    id_num=request.form['id_num']
    ticket_id=0
    return render_template('flight_purchase.html',airline=airline, flight_num=flight_num,dept_date=dept_date,dept_time=dept_time,arr_date=arr_date, arr_time=arr_time, dept_airport=dept_airport, flight_status=flight_status,id_num=id_num,price=base_price,ticket_id=ticket_id,username=username)

@app.route('/purchase_flight',methods=['GET','POST'])
def purchase_flight():
    pass


###############################################################################
###############################################################################
############################# Staff Pages #####################################


@app.route('/staff_home',methods=['GET', 'POST'])
def staff_home():
    if session.get('type')!='staff' or not session.get('username'):
        return redirect('/')
    username = session['username']
    return render_template('staff_home.html', email=username,username=username)


###############################################################################
###############################################################################
################################# Log Out #####################################

@app.route('/log_out')
def log_out():
    session['type']=None
    session['username']=None
    return redirect('/')


app.secret_key = 'Flight System Romee'
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
