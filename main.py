from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import random
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('SVG')

#Initialize the app from Flask
app=Flask(__name__,template_folder='template')


#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3308,
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
    query='SELECT ticket_id, airline_name, flight_num, dept_date, dept_time, arr_date, arr_time, dept_airport, arr_airport, flight_status, id_num, sold_price FROM ticket NATURAL JOIN purchase NATURAL JOIN flight WHERE email=%s AND ((dept_date=CURDATE() AND dept_time>=CURRENT_TIME()) OR dept_date>CURDATE())'
    cursor.execute(query,(email))
    data=cursor.fetchall()
    cursor.close()
    return render_template('customer_home_init.html',username=username,post1=data)

@app.route('/customer_cancel_flight',methods=['GET','POST'])
def customer_cancel_flight():
    ticket_id=request.form['ticket_id']
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    return render_template('customer_cancel_confirmation.html',ticket_id=ticket_id,airline_name=airline_name,flight_num=flight_num,dept_date=dept_date,dept_time=dept_time)

@app.route('/customer_cancel_confirmation',methods=['GET','POST'])
def customer_cancel_confirmation():
    ticket_id=request.form['ticket_id']
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']

    cursor=conn.cursor()
    query1='DELETE FROM ticket WHERE ticket_id=%s'
    query2='DELETE FROM purchase WHERE ticket_id=%s'
    cursor.execute(query2,(ticket_id))
    cursor.execute(query1,(ticket_id))
    conn.commit()
    cursor.close()

    return render_template('customer_cancel_success.html')
    




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
            view_query3='CREATE OR REPLACE VIEW temp_flight1 AS (SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
            
            '''
            query1='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))' '''

            view_query1='CREATE OR REPLACE VIEW cus_count AS (SELECT airline_name,flight_num,dept_date,dept_time,COUNT(ticket_id) AS cus_num FROM ticket GROUP BY airline_name,flight_num,dept_date,dept_time)'

            cursor.execute(view_query1)
            conn.commit()

            cursor.execute(view_query3, (departure, destination, dept_date, departure, dept_date, destination, destination, dept_date, departure, dept_date, departure, destination))
            conn.commit()

            query_dept='(SELECT airline_name,flight_num,dept_date,dept_time,arr_date,arr_time, dept_airport, arr_airport, IF(cus_num>seat_num*0.6,base_price*1.25, base_price) AS sold_price, flight_status,id_num FROM cus_count NATURAL JOIN temp_flight1 NATURAL JOIN airplane WHERE cus_num<seat_num) UNION\
                (SELECT airline_name,flight_num,dept_date,dept_time,arr_date,arr_time, dept_airport, arr_airport, base_price AS sold_price, flight_status,id_num FROM temp_flight1 WHERE NOT EXISTS (SELECT * FROM cus_count AS C WHERE C.airline_name=temp_flight1.airline_name AND C.flight_num=temp_flight1.flight_num AND C.dept_date=temp_flight1.dept_date AND C.dept_time=temp_flight1.dept_time))'

            cursor.execute(query_dept)
            data1=cursor.fetchall()

            view_query4='CREATE OR REPLACE VIEW temp_flight2 AS (SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'

            '''
            query2='(SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))' '''

            cursor.execute(view_query4, (destination, departure, return_date, destination, return_date, departure, departure, return_date, destination, return_date, destination, departure))
            conn.commit()

            query_re='(SELECT airline_name,flight_num,dept_date,dept_time,arr_date,arr_time, dept_airport, arr_airport, IF(cus_num>seat_num*0.6,base_price*1.25, base_price) AS sold_price, flight_status,id_num FROM cus_count NATURAL JOIN temp_flight2 NATURAL JOIN airplane WHERE cus_num<seat_num) UNION\
                (SELECT airline_name,flight_num,dept_date,dept_time,arr_date,arr_time, dept_airport, arr_airport, base_price AS sold_price, flight_status,id_num FROM temp_flight2 WHERE NOT EXISTS (SELECT * FROM cus_count AS C WHERE C.airline_name=temp_flight2.airline_name AND C.flight_num=temp_flight2.flight_num AND C.dept_date=temp_flight2.dept_date AND C.dept_time=temp_flight2.dept_time))'

            cursor.execute(query_re)

            data2=cursor.fetchall()
            cursor.close()

            return render_template('customer_home.html',post1=data1,post2=data2)

        else:
            return render_template('customer_home.html',error1='Please select the return date')

    else:
        cursor=conn.cursor()
        view_query2='CREATE OR REPLACE VIEW temp_flight AS ((SELECT * FROM flight WHERE dept_airport= %s AND arr_airport= %s AND dept_date = %s) UNION (SELECT * FROM flight WHERE dept_airport= %s AND dept_date= %s AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE arr_airport= %s AND dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE dept_date= %s AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s)))'

        view_query1='CREATE OR REPLACE VIEW cus_count AS (SELECT airline_name,flight_num,dept_date,dept_time,COUNT(ticket_id) AS cus_num FROM ticket GROUP BY airline_name,flight_num,dept_date,dept_time)'

        cursor.execute(view_query1)
        conn.commit()


        cursor.execute(view_query2, (departure, destination, dept_date, departure, dept_date, destination, destination, dept_date, departure, dept_date, departure, destination))
        conn.commit()

        query='(SELECT airline_name,flight_num,dept_date,dept_time,arr_date,arr_time, dept_airport, arr_airport, IF(cus_num>seat_num*0.6,base_price*1.25, base_price) AS sold_price, flight_status,id_num FROM cus_count NATURAL JOIN temp_flight NATURAL JOIN airplane WHERE cus_num<seat_num) UNION\
            (SELECT airline_name,flight_num,dept_date,dept_time,arr_date,arr_time, dept_airport, arr_airport, base_price AS sold_price, flight_status,id_num FROM temp_flight WHERE NOT EXISTS (SELECT * FROM cus_count AS C WHERE C.airline_name=temp_flight.airline_name AND C.flight_num=temp_flight.flight_num AND C.dept_date=temp_flight.dept_date AND C.dept_time=temp_flight.dept_time))'
        cursor.execute(query)
        data=cursor.fetchall()
        cursor.close()
        return render_template('customer_home.html',post1=data)

@app.route('/customer_search_flight_status',methods=['GET','POST'])
def customer_search_flight_status():
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
            return render_template('customer_home.html',post3=data)


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
    sold_price=request.form['sold_price']
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
    return render_template('flight_purchase.html',airline=airline, flight_num=flight_num,dept_date=dept_date,dept_time=dept_time,arr_date=arr_date, arr_time=arr_time, dept_airport=dept_airport, flight_status=flight_status,id_num=id_num,sold_price=sold_price,ticket_id=ticket_id,username=username,email=email)

@app.route('/purchase_flight',methods=['GET','POST'])
def purchase_flight():
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    price_origin=float(request.form['sold_price'])
    price=round(price_origin,2)
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

@app.route('/customer_previous',methods=['GET','POST'])
def customer_previous():
    email=session['email']
    username=session['username']

    cursor=conn.cursor()
    query='SELECT ticket_id,airline_name,flight_num,dept_date,dept_time,arr_date,arr_time,dept_airport,arr_airport,sold_price,flight_status,id_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchase WHERE email=%s AND ((dept_date=CURDATE() AND dept_time<CURRENT_TIME()) OR dept_date<CURDATE())'

    cursor.execute(query,(email))
    data=cursor.fetchall()
    cursor.close()
    return render_template('customer_previous_flight.html',post1=data,username=username)

@app.route('/rate_and_comment',methods=['GET','POST'])
def rate_and_comment():
    ticket_id=request.form['ticket_id']
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    email=session['email']
    username=session['username']

    arr_date=request.form['arr_date']
    arr_time=request.form['arr_time']
    dept_airprot=request.form['dept_airport']
    arr_airport=request.form['arr_airport']
    sold_price=request.form['sold_price']
    flight_status=request.form['flight_status']
    id_num=request.form['id_num']

    cursor=conn.cursor()

    query_pre='SELECT rate,cus_comment FROM previous_flight WHERE email=%s AND ticket_id=%s AND airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s'
    cursor.execute(query_pre,(email,ticket_id,airline_name,flight_num,dept_date,dept_time))
    data=cursor.fetchone()
    cursor.close()
    if data:
        pre_rate=data['rate']
        pre_comment=data['cus_comment']
        return render_template('rate_and_comment.html',ticket_id=ticket_id,airline_name=airline_name,flight_num=flight_num,dept_date=dept_date,dept_time=dept_time,arr_date=arr_date,arr_time=arr_time,dept_airprot=dept_airprot,arr_airport=arr_airport,sold_price=sold_price,flight_status=flight_status,id_num=id_num,username=username,pre_rate=pre_rate,pre_comment=pre_comment)
    else:
        return render_template('rate_and_comment.html',ticket_id=ticket_id,airline_name=airline_name,flight_num=flight_num,dept_date=dept_date,dept_time=dept_time,arr_date=arr_date,arr_time=arr_time,dept_airprot=dept_airprot,arr_airport=arr_airport,sold_price=sold_price,flight_status=flight_status,id_num=id_num,username=username)

@app.route('/rate_and_comment_form',methods=['GET','POST'])
def rate_and_comment_form():
    ticket_id=request.form['ticket_id']
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    email=session['email']
    new_rate=int(request.form['rate'])
    new_comment=request.form['comment']

    cursor=conn.cursor()

    query_pre='SELECT rate,cus_comment FROM previous_flight WHERE email=%s AND ticket_id=%s AND airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s'
    cursor.execute(query_pre,(email,ticket_id,airline_name,flight_num,dept_date,dept_time))
    data=cursor.fetchone()
    cursor.close()

    if data:
        cursor=conn.cursor()
        up_query='UPDATE previous_flight SET cus_comment=%s, rate=%s WHERE ticket_id=%s AND email=%s AND airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s'
        cursor.execute(up_query,(new_comment,new_rate,ticket_id,email,airline_name,flight_num,dept_date,dept_time))
        conn.commit()
        cursor.close()
        return render_template('rate_success.html')

    else:
        cursor=conn.cursor()
        print(ticket_id,email,airline_name,flight_num,dept_date,dept_time,new_comment,new_rate)
        in_query='INSERT INTO previous_flight VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(in_query,(ticket_id,email,airline_name,flight_num,dept_date,dept_time,new_comment,new_rate))
        conn.commit()
        cursor.close()
        return render_template('rate_success.html')

@app.route('/customer_spending',methods=['GET','POST'])
def customer_spending():
    username=session['username']

    today_date=datetime.today().date()
    month_today=today_date.replace(day=1)
    today_date_str=today_date.strftime("%y-%m-%d")

    six_months = date.today() + relativedelta(months=-6)
    month_six_month=six_months.replace(day=1)
    six_month_str=month_six_month.strftime("%y-%m-%d")

    a_year=date.today() + relativedelta(years=-1)
    month_a_year=a_year.replace(day=1)
    a_year_str=month_a_year.strftime("%y-%m-%d")

    email=session['email']

    cursor=conn.cursor()
    year_query='SELECT SUM(sold_price) AS spending FROM purchase WHERE email=%s AND purchase_date<=%s AND purchase_date>=%s'
    cursor.execute(year_query,(email,today_date_str,a_year_str))
    data1=cursor.fetchone()
    if data1:
        total_spending=data1['spending']

        month_query='SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, SUM(sold_price) AS spending FROM purchase WHERE email=%s AND purchase_date<=%s AND purchase_date>=%s GROUP BY YEAR(purchase_date),MONTH(purchase_date)'
        cursor.execute(month_query,(email,today_date_str,six_month_str))
        data2=cursor.fetchall()

        cursor.close()
        if data2:
            return render_template('customer_spending.html',username=username,total_spending=total_spending,data2=data2)
        else:
            return render_template('customer_spending.html',username=username,total_spending=total_spending)

    else:
        cursor.close()
        return render_template('customer_spending.html',username=username)

@app.route('/customer_spending_form',methods=['GET','POST'])
def customer_spending_form():
    username=session['username']
    email=session['email']
    start_date=request.form['start_date']
    end_date=request.form['end_date']

    cursor=conn.cursor()

    total_query='SELECT SUM(sold_price) AS spending FROM purchase WHERE email=%s AND purchase_date>%s AND purchase_date<%s'
    cursor.execute(total_query,(email,start_date,end_date))
    data1=cursor.fetchone()
    if data1:
        total_spending=data1['spending']

        month_query='SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, SUM(sold_price) AS spending FROM purchase WHERE email=%s AND purchase_date<=%s AND purchase_date>=%s GROUP BY YEAR(purchase_date),MONTH(purchase_date)'
        cursor.execute(month_query,(email,end_date,start_date))
        data2=cursor.fetchall()
        
        lists=[[],[]]
        for row in data2:
            lists[0].append(str(row['year'])+str(row['month']))
            lists[1].append(float(row['spending']))

        x=lists[0]
        y=lists[1]
        
        plt.bar(x,y,width=0.5,bottom=0,align='edge',color='#1565C0',edgecolor ='#6598d3',linewidth=2)
        plt.title("spending by month",size=26)
        plt.xlabel('month',size=18)
        plt.ylabel('spending',size=18)

        plt.savefig('template/customer_spending.png')
        cursor.close()

        return render_template('customer_spending.html',username=username,total_spending=total_spending,data2=data2)

    else:
        return render_template('customer_spending.html',username=username)






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
    query1='(SELECT * FROM flight WHERE airline_name=%s AND dept_airport= %s AND arr_airport= %s AND (dept_date BETWEEN %s AND %s)) UNION (SELECT * FROM flight WHERE airline_name=%s AND dept_airport= %s AND (dept_date BETWEEN %s AND %s) AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE airline_name=%s AND arr_airport= %s AND (dept_date BETWEEN %s AND %s) AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE airline_name=%s AND (dept_date BETWEEN %s AND %s) AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
    cursor.execute(query1,(airline_name,departure,destination,start_date,end_date, airline_name,departure,start_date,end_date,destination, airline_name,destination,start_date,end_date,departure, airline_name,start_date,end_date,departure,destination))

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
    if session['airline']==None or session['type']!='staff':
        return redirect('/')
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
    print(airline_name,id_num)
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
    if session['airline']==None or session['type']!='staff':
        return redirect('/')
    airline_name=session['airline']
    username=session['username']
    return render_template('change_flight_status.html',username=username,airline_name=airline_name)

@app.route('/search_flight_change_status',methods=['GET','POST'])
def search_flight_change_status():
    if session['airline']==None or session['type']!='staff':
        return redirect('/')
    username=session['username']
    airline_name=session['airline']
    #airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    cursor=conn.cursor()
    query1='SELECT * FROM flight WHERE airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s'
    cursor.execute(query1,(airline_name,flight_num,dept_date,dept_time))
    post1=cursor.fetchall()
    cursor.close()
    return render_template('change_flight_status.html',username=username,airline_name=airline_name,post1=post1)

@app.route('/change_status_confirm',methods=['GET','POST'])
def change_status_confirm():
    airline_name=request.form['airline_name']
    flight_num=request.form['flight_num']
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']
    new_status=request.form['status']
    cursor=conn.cursor()
    up_query='UPDATE flight SET flight_status=%s WHERE airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s'
    cursor.execute(up_query,(new_status,airline_name,flight_num,dept_date,dept_time))
    conn.commit()
    cursor.close()
    return render_template('change_status_success.html')


@app.route('/add_airplane',methods=['GET','POST'])
def add_airplane():
    if session['airline']==None or session['type']!='staff':
        return redirect('/')
    airline=session['airline']
    return render_template('add_airplane.html',airline=airline)

@app.route('/add_airplane_form',methods=['GET','POST'])
def add_airplane_form():
    if session['airline']==None or session['type']!='staff':
        return redirect('/')
    airline_name=request.form['airline_name']
    id_num=request.form['id_num']
    seat_num=int(request.form['seat_num'])
    manu_company=request.form['manu_company']
    age=int(request.form['age'])

    cursor=conn.cursor()
    query1='SELECT * FROM airplane WHERE airline_name=%s AND id_num=%s'
    cursor.execute(query1,(airline_name,id_num))
    data1=cursor.fetchall()
    if data1:
        cursor.close()
        return render_template('add_airplane.html',error='Airplane already existed')
    in_query='INSERT INTO airplane VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(in_query,(airline_name,id_num,seat_num,manu_company,age))
    conn.commit()
    cursor.close()

    cursor=conn.cursor()
    query='SELECT * FROM airplane WHERE airline_name=%s'
    cursor.execute(query,(airline_name))
    data=cursor.fetchall()
    cursor.close()
    return render_template('add_airplane_success.html',data=data,airline_name=airline_name)
    

@app.route('/add_airport',methods=['GET','POST'])
def add_airport():
    if session['airline']==None or session['type']!='staff':
        return redirect('/')
    return render_template('add_airport.html')

@app.route('/add_airport_form',methods=['GET','POST'])
def add_airport_form():
    name=request.form["name"]
    city=request.form['city']
    country=request.form['country']
    airport_type=request.form['type']
    if len(name)!=3:
        return render_template('add_airport.html',error='Please enter valid airport name')
    cursor=conn.cursor()
    query1='SELECT * FROM airport WHERE name=%s'
    cursor.execute(query1,(name))
    data1=cursor.fetchall()
    if data1:
        cursor.close()
        return render_template('add_airport.html',error='Airport already existed')
    in_query='INSERT INTO airport VALUES (%s,%s,%s,%s)'
    cursor.execute(in_query,(name,city,country,airport_type))
    conn.commit()
    cursor.close()
    return render_template('add_airport_success.html')


@app.route('/flight_ratings',methods=['GET','POST'])
def flight_rating():
    if session.get('type')!='staff' or not session.get('username'):
        return redirect('/')
    airline=session['airline']
    username = session['username']
    today_date=datetime.today().date()
    start_date=today_date-timedelta(30)
    today_date_str=today_date.strftime("%y-%m-%d")
    start_date_str=start_date.strftime("%y-%m-%d")

    cursor=conn.cursor()
    query='SELECT * FROM flight WHERE airline_name= %s AND (dept_date BETWEEN %s AND %s)' 
    cursor.execute(query,(airline,start_date_str,today_date_str))
    data=cursor.fetchall()
    cursor.close()
    
    return render_template('flight_rating_home.html',airline=airline, username=username, post1=data)

@app.route('/search_rate_comment',methods=['GET','POST'])
def search_rate_comment():
    if session.get('type')!='staff' or not session.get('username'):
        return redirect('/')

    airline_name=session['airline']
    username=session['username']
    departure=request.form['departure']
    destination=request.form['destination']
    start_date=request.form['start_date']
    end_date=request.form['end_date']

    cursor=conn.cursor()
    query1='(SELECT * FROM flight WHERE airline_name=%s AND dept_airport= %s AND arr_airport= %s AND (dept_date BETWEEN %s AND %s)) UNION (SELECT * FROM flight WHERE airline_name=%s AND dept_airport= %s AND (dept_date BETWEEN %s AND %s) AND arr_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE airline_name=%s AND arr_airport= %s AND (dept_date BETWEEN %s AND %s) AND dept_airport IN (SELECT name FROM airport WHERE city= %s)) UNION (SELECT * FROM flight WHERE airline_name=%s AND (dept_date BETWEEN %s AND %s) AND dept_airport IN (SELECT name FROM airport WHERE city= %s) AND arr_airport IN (SELECT name FROM airport WHERE city = %s))'
    cursor.execute(query1,(airline_name,departure,destination,start_date,end_date, airline_name,departure,start_date,end_date,destination, airline_name,destination,start_date,end_date,departure, airline_name,start_date,end_date,departure,destination))

    data=cursor.fetchall()
    cursor.close()

    return render_template('flight_rating_home.html',airline=airline_name,username=username,post1=data)

@app.route('/view_rate_and_comment',methods=['GET','POST'])
def view_rate_and_comment():
    if session.get('type')!='staff' or not session.get('username'):
        return redirect('/')
    username=session['username']
    airline_name=session['airline']
    flight_num=request.form['flight_num']
    print(flight_num)
    dept_date=request.form['dept_date']
    dept_time=request.form['dept_time']

    cursor=conn.cursor()
    average_query='SELECT sum(rate)/(COUNT(rate)) AS average FROM previous_flight WHERE airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s GROUP BY airline_name,flight_num,dept_date,dept_time'
    cursor.execute(average_query,(airline_name,flight_num,dept_date,dept_time))
    data1=cursor.fetchone()
    if data1:
        average_rate=data1['average']

        all_query='SELECT email,rate,cus_comment FROM previous_flight WHERE airline_name=%s AND flight_num=%s AND dept_date=%s AND dept_time=%s'
        cursor.execute(all_query,(airline_name,flight_num,dept_date,dept_time))
        data2=cursor.fetchall()
        cursor.close()

        return render_template('rating_and_comment.html',username=username,flight_num=flight_num,dept_date=dept_date,dept_time=dept_time,average=average_rate,data2=data2)
    else:
        return render_template('rating_and_comment.html',username=username,flight_num=flight_num,dept_date=dept_date,dept_time=dept_time)


@app.route('/frequent_customer',methods=['GET','POST'])
def frequent_customer():
    username=session['username']
    airline_name=session['airline']
    today_date=datetime.today().date()
    today_date_str=today_date.strftime("%y-%m-%d")

    a_year=date.today() + relativedelta(years=-1)
    a_year_str=a_year.strftime("%y-%m-%d")

    cursor=conn.cursor()
    query='SELECT email,COUNT(ticket_id) AS num FROM purchase NATURAL JOIN ticket WHERE airline_name=%s AND purchase_date>%s AND purchase_date<=%s GROUP BY email ORDER BY num DESC'
    cursor.execute(query,(airline_name,a_year_str,today_date_str))
    most_fre=cursor.fetchone()
    email=most_fre['email']
    num=most_fre['num']
    cursor.close()

    return render_template('frequent_customer.html',username=username,email=email,num=num)

@app.route('/search_customer_flight',methods=['GET','POST'])
def search_customer_flight():
    airline_name=session['airline']
    username=session['username']
    email=request.form['email']

    cursor=conn.cursor()
    query='SELECT airline_name,flight_num,dept_date,dept_time,arr_date,arr_time,dept_airport,arr_airport,base_price,sold_price,flight_status,id_num FROM ticket NATURAL JOIN purchase NATURAL JOIN flight WHERE email=%s AND airline_name=%s'
    cursor.execute(query,(email,airline_name))
    data=cursor.fetchall()
    cursor.close()

    return render_template('frequent_customer.html',username=username,post1=data)




@app.route('/view_report',methods=['GET','POST'])
def view_report():
    username=session['username']
    airline_name=session['airline']

    today_date=datetime.today().date()
    today_date_str=today_date.strftime("%y-%m-%d")

    one_months = date.today() + relativedelta(months=-1)
    one_month_str=one_months.strftime("%y-%m-%d")

    a_year=date.today() + relativedelta(years=-1)
    a_year_str=a_year.strftime("%y-%m-%d")

    cursor=conn.cursor()
    query_month='SELECT COUNT(ticket_id) AS month_sold FROM purchase NATURAL JOIN ticket WHERE purchase_date>%s AND purchase_date<=%s AND airline_name=%s'
    cursor.execute(query_month,(one_month_str,today_date_str,airline_name))
    data1=cursor.fetchone()

    query_year='SELECT COUNT(ticket_id) AS year_sold FROM purchase NATURAL JOIN ticket WHERE purchase_date>%s AND purchase_date<=%s AND airline_name=%s'
    cursor.execute(query_year,(a_year_str,today_date_str,airline_name))
    data2=cursor.fetchone()
    if data2:
        year_report=data2['year_sold']

        query_all='SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, COUNT(ticket_id) AS monthly FROM purchase NATURAL JOIN ticket WHERE purchase_date>%s AND purchase_date<=%s AND airline_name=%s GROUP BY YEAR(purchase_date),MONTH(purchase_date)'
        cursor.execute(query_all,(a_year_str,today_date_str,airline_name))
        data3=cursor.fetchall()

        cursor.close()
        if data1:
            month_report=data1['month_sold']
            return render_template('reports.html',username=username,month_report=month_report,year_report=year_report,data2=data3)
        else:
            return render_template('reports.html',username=username,year_report=year_report,data2=data3)

    else:
        return render_template('reports.html',username=username)

@app.route('/search_report',methods=['GET','POST'])
def search_report():
    airline_name=session['airline']
    username=session['username']
    start_date=request.form['start_date']
    end_date=request.form['end_date']

    cursor=conn.cursor()
    query_total='SELECT COUNT(ticket_id) AS year_sold FROM purchase NATURAL JOIN ticket WHERE purchase_date>%s AND purchase_date<=%s AND airline_name=%s'
    cursor.execute(query_total,(start_date,end_date,airline_name))
    data1=cursor.fetchone()
    if data1:
        year_report=data1['year_sold']

        query_all='SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, COUNT(ticket_id) AS monthly FROM purchase NATURAL JOIN ticket WHERE purchase_date>%s AND purchase_date<=%s AND airline_name=%s GROUP BY YEAR(purchase_date),MONTH(purchase_date)'
        cursor.execute(query_all,(start_date,end_date,airline_name))
        data2=cursor.fetchall()

        cursor.close()
        return render_template('reports.html',username=username,year_report=year_report,data2=data2)

    else:
        cursor.close()
        return render_template('reports.html',username=username)



@app.route('/view_revenue',methods=['GET','POST'])
def view_revenue():
    pass



###############################################################################
###############################################################################
################################# Log Out #####################################

@app.route('/log_out')
def log_out():
    username=session['username']
    session['type']=None
    session['username']=None
    session['email']=None
    session['airline']=None
    return render_template('goodbye.html',username=username)

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
