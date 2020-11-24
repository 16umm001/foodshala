from flask import Flask, request, url_for, redirect, render_template , session
import mysql.connector
from database_detail import database_name



mydb = mysql.connector.connect(
  host="<host name>",
  user="<database user name>",
  passwd="<Enter database password>",
  database="mydatabase"
)




mycursor = mydb.cursor()
app = Flask(__name__)
app.secret_key = "foodshala"

@app.route('/')
def home():
  if session.get('who') is 'hotel':
    return redirect(url_for('restaurant_home'))
  query = "SELECT * from menu"
  mycursor.execute(query)
  data = mycursor.fetchall()
  print("aaaaaaaaa")
  
  return render_template('home.html', data = data)

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('userlogin.html')

@app.route('/hotellogin', methods=['GET', 'POST'])
def hotellogin():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('hotellogin.html')


@app.route('/usersignup', methods=['GET', 'POST'])
def usersignup():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('usersignup.html')

@app.route('/hotelsignup', methods=['GET', 'POST'])
def hotelsignup():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('hotelsignup.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
  if request.method == 'POST':
    uname = request.form['username']
    fname = request.form['fname']
    mobile = request.form['mobile']
    pref = request.form['pref']
    password = request.form['password']
    cpassword = request.form['cpassword']
    
    sql = "INSERT INTO customers12 (uname, fname , mobile,pref,password) VALUES (%s, %s,%s,%s,%s)"
    val = (uname ,fname, mobile ,pref, password)
    mycursor.execute(sql, val)
    mydb.commit()
    return render_template('userlogin.html' , uname = uname)
  return render_template('userlogin.html')

@app.route('/ressignup', methods = ['GET','POST'])
def ressignup():
  if request.method == 'POST':
    uname = request.form['uname']
    rname = request.form['restaurantname']
    mobile = request.form['mobile']
    address = request.form['address']
    password = request.form['password']
    cpassword = request.form['cpassword']
    
    sql = "INSERT INTO restaurant (uname, rname , mobile,address,password) VALUES (%s, %s,%s,%s,%s)"
    val = (uname ,rname, mobile ,address, password)
    mycursor.execute(sql, val)
    mydb.commit()
    return render_template('hotellogin.html')
  return render_template('hotellogin.html')

@app.route('/hotelLogin', methods = ['GET','POST'])
def hotelLogin():
  if request.method == 'POST':
    uname1 = request.form['username']
    password1 = request.form['password']
    
    sql = "SELECT password FROM restaurant WHERE uname = %s"
    val = (uname1,)
    mycursor.execute(sql,val)
    result = mycursor.fetchone()
    for i in result:
      if password1 == i:
        session.clear()
        session['uname'] = uname1
        session['who'] = "hotel"
        return redirect('/restaurant_home')
  return render_template('hotellogin.html' , text = "id password do not match")


@app.route('/userLogin', methods = ['GET','POST'])
def userLogin():
  if request.method == 'POST':
    uname2 = request.form['username']
    password2 = request.form['password']

    sql = "SELECT password,pref FROM customers12 WHERE uname = %s"
    val = (uname2,)
    mycursor.execute(sql,val)
    result1 = mycursor.fetchone()
    if result1[0] == password2:
      session.clear()
      session['uname'] = uname2
      session['who'] = "user"
      session['pref'] = result1[1]
      return redirect(url_for('user_home'))
  return render_template('userlogin.html' , text = "id password do not match")

@app.route('/addmenu', methods = ['GET','POST'])
def addmenu():
  if request.method == 'POST':
    itemname = request.form['itemname']
    itemdetail = request.form['detail']
    price = request.form['price']
    itemtype = request.form['foodtype']

    sql3 = "INSERT INTO menu (itemname, itemdetail , price,itemtype,hotelid) VALUES (%s,%s,%s,%s,%s)"
    val3 = (itemname, itemdetail , price,itemtype,session.get('uname'))
    mycursor.execute(sql3, val3)
    mydb.commit()
    return render_template('add_menu.html' )
  return render_template('add_menu.html')

@app.route('/showmenutohotel', methods = ['GET','POST'])
def showmenutohotel():
  hotel_id1 = session.get('uname')
  query = "SELECT * from menu WHERE hotelid = %s"
  va = (hotel_id1,)
  mycursor.execute(query , va)
  data = mycursor.fetchall()
  return render_template('hotelsmenu.html', data = data)


@app.route('/hotellogout', methods = ['GET','POST'])
def hotellogout():
  session.pop('uname' , None)
  session.pop('who' , None)
  session.clear()
  return render_template('hotellogin.html')

@app.route('/orderproduct/<int:id>', methods = ['GET','POST'])
def orderproduct(id):
  if session.get('who')=='hotel':
    return render_template('restaurants_home.html' , msg = "You are logged in as Hotel admin.Please login as user to order")

  elif session.get('uname') is None:
    return render_template('userlogin.html')

  username = session.get('uname')
  query_order = "SELECT * from menu WHERE ID = %s"
  val_order = (id,)
  mycursor.execute(query_order , val_order)
  data = mycursor.fetchone()

  sql_order = "INSERT INTO orders (rname, uname , product) VALUES (%s, %s,%s)"
  val_order = (data[4] ,username, data[0])
  mycursor.execute(sql_order, val_order)
  mydb.commit()

  return redirect(url_for('user_home'))


@app.route('/restaurant_home', methods = ['GET','POST'])
def restaurant_home():
  query = "SELECT * from menu"
  mycursor.execute(query)
  data = mycursor.fetchall()
  return render_template('restaurants_home.html',data = data)

@app.route('/user_home' , methods = ['GET' , 'POST'])
def user_home():
  if session.get('who') is 'user':
    return redirect(url_for('user_home'))
  query_pref = "SELECT * from menu WHERE itemtype = %s"
  prefe = session.get('pref')
  pref_val = (prefe,)
  mycursor.execute(query_pref , pref_val)
  data = mycursor.fetchall()
  return render_template('user_home.html', data = data)


@app.route('/user_logout', methods = ['GET','POST'])
def user_logout():
  session.pop('uname' , None)
  session.pop('who' , None)
  session.pop('pref' ,None)
  session.clear()
  return redirect('/')

@app.route('/orders_list' , methods = ['GET','POST'])
def orders_list():
  uname11 = session.get('uname')
  sql11 = "SELECT * FROM orders WHERE rname = %s"
  val11 = (uname11,)
  mycursor.execute(sql11 , val11)
  data = mycursor.fetchall()
  return render_template('order_list.html', data = data)



if __name__ == '__main__':
   app.run(debug = True)
