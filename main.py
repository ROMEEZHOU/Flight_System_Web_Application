from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime, date, timedelta
import random

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
    session['type']=None
    session['username']=None
    session['email']=None
    session['airline']=None
    return render_template('index.html',posts='')

@app.route('/SearchFlight1',methods=['GET', 'POST'])
def SearchFlight1():
    departure = request.form['departure']
    destination=request.form['destination']
    dept_date=request.form['dept_date']
    return_date=request.form['return_date']
    today_date=datetime.today().date()
    dept_date_obj=datetime.strptime(dept_date, '%Y-%m-%d').date()
    if dept_date_obj<today_date:
        return render_template('index.html',error1='Please select a valid departure date')
    if 'round_trip' in request.form:
        if return_date!='':
            return_date_obj=datetime.strptime(return_date, '%Y-%m-%d').date()
            if return_date_obj<dept_date_obj:
                return render_template('index.html',error1='Please select valid departure date and return date')
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
            return render_template('index.html',error1='Please select the return date')

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
            return render_template('index.html',error2='Please enter either departure date or arrival date')
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
        cursor.close()
        return render_template('customer_register.html', error = error)
    if not isinstance(building_number, int):
        error = "Building number must be an integer"
        cursor.close()
        return render_template('customer_register.html', error = error)
        
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, MD5(%s), %s , %s, %s, %s, %s, %s, %s, %s, %s)'
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
    cursor.execute(query2, (airline))
    data2 = cursor.fetchone()
    if not data2:
        error = 'This airline does not exist'
        cursor.close()
        return render_template('staff_register.html', error = error)

    if(data1):
    	#If the previous query returns data, then user exists
        error = "This username is been already existed"
        conn.commit()
        cursor.close()
        return render_template('staff_register.html', error = error)

        
    else:
        
        ins = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s , %s, %s)'
        cursor.execute(ins, (username, user_password, first_name, last_name, date_of_birth, airline))
        for phone_n in phone_list:
            ins_phone = 'INSERT INTO staff_phone VALUES(%s, %s)'
            cursor.execute(ins_phone,(username,phone_n))

        for e in email_list:
            ins_email='INSERT INTO staff_email VALUES(%s, %s)'
            cursor.execute(ins_email,(username,e))

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
    query = 'SELECT name FROM customer WHERE email = %s and customer_password = MD5(%s)'
    cursor.execute(query, (email, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        session['type']='customer'
        session['email']=email
        session['username'] = data['name']
        print(session['email'])
        return redirect(url_for('customer_home_init'))
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
        session['type'] = 'staff'
        session['airline']=data['airline']
        session['username'] = username
        return redirect(url_for('staff_home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('staff_login.html', error=error)


###############################################################################
###############################################################################
########################## Customer Home Pages ################################

@app.route('/customer_home_init',methods=['GET', 'POST'])
def customer_home_init():
    if session.get('type')!='customer' or not session.get('username'):
        return redirect('/')
    username=session['username']
    email = session['email']
    print(email)
    cursor=conn.cursor()
    query='SELECT airline_name, flight_num, dept_date, dept_time, arr_date, arr_time, dept_airport, arr_airport, flight_status, id_num FROM ticket NATURAL JOIN purchase NATURAL JOIN flight WHERE email=%s AND ((dept_date=CURDATE() AND dept_time>=CURRENT_TIME()) OR dept_date>CURDATE())'
    cursor.execute(query,(email))
    data=cursor.fetchall()
    cursor.close()
    return render_template('customer_home_init.html',username=username,post1=data)




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
    today_date=datetime.today().date()
    dept_date_obj=datetime.strptime(dept_date, '%Y-%m-%d').date()
    if dept_date_obj<today_date:
        return render_template('customer_home.html',error1='Please select a valid departure date')
    if 'round_trip' in request.form:
        if return_date!='':
            return_date_obj=datetime.strptime(return_date, '%Y-%m-%d').date()
            if return_date_obj<dept_date_obj:
                return render_template('customer_home.html',error1='Please select valid departure date and return date')
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
            return render_template('customer_home.html',error1='Please select the return date')

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
    email=session['email']
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
    ticket_id=generate_random_str()
    cursor=conn.cursor()
    id_query='SELECT * FROM ticket WHERE ticket_id=%s'
    cursor.execute(id_query,(ticket_id))
    data=cursor.fetchone()
    while data:
        ticket_id=generate_random_str()
        cursor.execute(id_query,(ticket_id))
        data=cursor.fetchall()
    
    cursor.close()
    return render_template('flight_purchase.html',airline=airline, flight_num=flight_num,dept_date=dept_date,dept_time=dept_time,arr_date=arr_date, arr_time=arr_time, dept_airport=dept_airport, flight_status=flight_status,id_num=id_num,price=base_price,ticket_id=ticket_id,username=username,email=email)

@app.route('/purchase_flight',methods=['GET','POST'])
def purchase_flight():
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    price=request.form['price']
    ticket_id=request.form['ticket_id']
    email=request.form['email']
    card_type=request.form['card_type']
    card_number=request.form['card_number']
    name_on_card=request.form['name_on_card']
    expiration_date=request.form['expiration_date']
    today=date.today()
    purchase_date=today.strftime("%y-%m-%d")
    now=datetime.now()
    purchase_time=now.strftime("%H:%M:%S")
    
    print(ticket_id,airline_name,flight_num,dept_date,dept_time)
    cursor=conn.cursor()
    
    query_ticket='INSERT INTO ticket VALUES(%s,%s,%s,%s,%s)'
    cursor.execute(query_ticket,(ticket_id,airline_name,flight_num,dept_date,dept_time))

    print(ticket_id,email,price,card_type,card_number,name_on_card,expiration_date,purchase_date,purchase_time)
    
    query_purchase='INSERT INTO purchase VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(query_purchase,(ticket_id,email,price,card_type,card_number,name_on_card,expiration_date,purchase_date,purchase_time))
    
    conn.commit()
    cursor.close()
    return render_template('purchase_success.html')

###############################################################################
###############################################################################
############################# Staff Pages #####################################


@app.route('/staff_home',methods=['GET', 'POST'])
def staff_home():
    if session.get('type')!='staff' or not session.get('username'):
        return redirect('/')
    airline=session['airline']
    username = session['username']
    today_date=datetime.today().date()
    end_date=today_date+timedelta(30)
    today_date_str=today_date.strftime("%y-%m-%d")
    end_date_str=end_date.strftime("%y-%m-%d")

    cursor=conn.cursor()
    query='SELECT * FROM flight WHERE airline_name= %s AND (dept_date BETWEEN %s AND %s)' 
    cursor.execute(query,(airline,today_date_str,end_date_str))
    data=cursor.fetchall()
    cursor.close()
    
    return render_template('staff_home.html',airline=airline, username=username, post1=data)

@app.route('/staff_view_flight', methods=['GET','POST'])
def staff_view_flight():
    airline=session['airline']
    username=session['username']
    departure=request.form['departure']
    destination=request.form['destination']
    start_date=request.form['start_date']
    end_date=request.form['end_date']

    cursor=conn.cursor()
    query1='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND (dept_date BETWEEN %s AND %s)) UNION (SELECT * FROM flight WHERE dept_airport= %s AND (dept_date BETWEEN %s AND %s) AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND (dept_date BETWEEN %s AND %s) AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE (dept_date BETWEEN %s AND %s) AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
    cursor.execute(query1,(departure,destination,start_date,end_date,departure,start_date,end_date,destination,destination,start_date,end_date,departure,start_date,end_date,departure,destination))

    data=cursor.fetchall()
    cursor.close()
    
    return render_template('staff_home.html',airline=airline, username=username, post1=data)

    '''
    if departure=='' and destination==''  and start_date=='' and end_date=='':
        return render_template('staff_home.html',airline=airline, username=username, error='Please enter at least one filter')
    elif departure=='' and destination=='' and start_date=='' and end_date!='':
        cursor=conn.cursor()
        query='SELECT * FROM flight WHERE airline_name= %s AND (dept_date < %s)' 
        cursor.execute(query,(airline,end_date))
        data=cursor.fetchall()
        cursor.close() 
        return render_template('staff_home.html',airline=airline, username=username, post1=data)

    elif departure=='' and destination=='' and end_date=='' and start_date!='':
        cursor=conn.cursor()
        query='SELECT * FROM flight WHERE airline_name= %s AND (dept_date > %s)' 
        cursor.execute(query,(airline,start_date))
        data=cursor.fetchall()
        cursor.close() 
        return render_template('staff_home.html',airline=airline, username=username, post1=data)
    
    elif departure=='' and destination=='' and end_date!='' and start_date!='':
        cursor=conn.cursor()
        query='SELECT * FROM flight WHERE airline_name= %s AND (dept_date BETWEEN %s AND %s)' 
        cursor.execute(query,(airline,start_date,end_date))
        data=cursor.fetchall()
        cursor.close() 
        return render_template('staff_home.html',airline=airline, username=username, post1=data)

    elif departure!='' and destination==''  and start_date=='' and end_date=='':
        cursor=conn.cursor()
        query1='(SELECT * FROM flight WHERE dept_airport= %s) UNION (SELECT * FROM flight WHERE dept_airport IN (SELECT name FROM airport WHERE city= %s)) '
        cursor.execute(query1,(departure,departure))   
        data=cursor.fetchall()
        cursor.close() 
        return render_template('staff_home.html',airline=airline, username=username, post1=data)

    elif departure=='' and destination!=''  and start_date=='' and end_date=='':
        cursor=conn.cursor()
        query1='(SELECT * FROM flight WHERE arr_airport= %s) UNION (SELECT * FROM flight WHERE arr_airport IN (SELECT name FROM airport WHERE city= %s)) '
        cursor.execute(query1,(destination,destination))   
        data=cursor.fetchall()
        cursor.close() 
        return render_template('staff_home.html',airline=airline, username=username, post1=data)

    elif departure!='' and destination!=''  and start_date=='' and end_date=='':
        cursor=conn.cursor()
        query1='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
        cursor.execute(query1,(departure,destination,departure,destination,destination,departure,departure,destination))
        data=cursor.fetchall()
        cursor.close() 
        return render_template('staff_home.html',airline=airline, username=username, post1=data)

    elif departure!='' and destination!=''  and start_date!='' and end_date=='':'''

@app.route('/view_customer',methods=['GET','POST'])
def view_customer():
    flight_num=request.form['flight_num']
    airline_name=request.form['airline_name']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    airline=session['airline']
    username=session['username']

    cursor=conn.cursor()
    query='SELECT email,name,building_num,street,city,state,phone_num,passport_num,passport_expiration,passport_country,date_of_birth FROM purchase NATURAL JOIN ticket NATURAL JOIN customer WHERE airline_name= %s AND flight_num= %s AND dept_date= %s AND dept_time= %s'
    cursor.execute(query,(airline_name,flight_num,dept_date,dept_time))
    data=cursor.fetchall()
    cursor.close()
    
    return render_template('view_customer.html',airline=airline, flight_num=flight_num, username=username, post1=data)

@app.route('/add_flight',methods=['GET','POST'])
def add_flight():
    if session['airline']==None or session['type']!='staff':
        return redirect('/')
    airline=session['airline']
    return render_template('add_flight.html',airline=airline)

@app.route('/add_flight_form',methods=['GET','POST'])
def add_flight_form():
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    arr_date=request.form['arr_date']
    arr_time=request.form['arr_time']
    dept_airport=request.form['dept_airport']
    arr_airport=request.form['arr_airport']
    base_price=int(request.form['base_price'])
    flight_status=request.form['flight_status']
    id_num=request.form['id_num']

    cursor=conn.cursor()
    query1='SELECT * FROM flight WHERE airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s'
    cursor.execute(query1,(airline_name,flight_num,dept_date,dept_time))
    data1=cursor.fetchall()
    if data1:
        cursor.close()
        return render_template('add_flight.html',error='Flight already exists')
    query2='SELECT * FROM airport WHERE name=%s'
    cursor.execute(query2,(dept_airport))
    data2=cursor.fetchall()
    if not data2:
        cursor.close()
        return render_template('add_flight.html',error='Departure airport does not exist')
    cursor.execute(query2,(arr_airport))
    data3=cursor.fetchall()
    if not data3:
        cursor.close()
        return render_template('add_flight.html',error='Arrival airport does not exist')
    query3='SELECT * FROM airplane WHERE airline_name=%s AND id_num=%s'
    cursor.execute(query3,(airline_name,id_num))
    data4=cursor.fetchall()
    if not data4:
        cursor.close()
        return render_template('add_flight.html',error='Airplane does not exist')

    in_query='INSERT INTO flight VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(in_query,(airline_name,flight_num,dept_date,dept_time,arr_date,arr_time,dept_airport,arr_airport,base_price,flight_status,id_num))
    conn.commit()
    cursor.close()

    return render_template('add_flight_success.html')


@app.route('/change_flight_status',methods=['GET','POST'])
def change_flight_status():
    pass

@app.route('/add_airplane',methods=['GET','POST'])
def add_airplane():
    pass

@app.route('/add_airport',methods=['GET','POST'])
def add_airport():
    pass

@app.route('/flight_rating',methods=['GET','POST'])
def flight_rating():
    pass

@app.route('/frequent_customer',methods=['GET','POST'])
def frequent_customer():
    pass

@app.route('/view_report',methods=['GET','POST'])
def view_report():
    pass

@app.route('/view_revenue',methods=['GET','POST'])
def view_revenue():
    pass



###############################################################################
###############################################################################
################################# Log Out #####################################

@app.route('/log_out')
def log_out():
    session['type']=None
    session['username']=None
    session['email']=None
    session['airline']=None
    return redirect('/')

def generate_random_str(randomlength=29):
    random_str =''
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    for i in range(randomlength):
        random_str +=base_str[random.randint(0, length)]
    return random_str


app.secret_key = 'Flight System Romee'
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
