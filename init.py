from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import re
import mysql.connector
import time
import datetime 

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
					port='8889',
					user='root',
					password='root',
					database='Auction')


@app.route('/')
def hello():
 return render_template('login.html')


#Define route for login
@app.route('/login')
def login():
 return render_template('login.html')



#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')



@app.route('/logout')
def logout():
	logout_user(current_user)
	return redirect('/login.html')




#----------------------register------------------------------------------

@app.route('/cus_register', methods=['GET', 'POST'])
def cus_register():
	email = request.form['email']
	name = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()
	query = "SELECT * FROM Customer WHERE customerEmail = \'{}\'"
	cursor.execute(query.format(email, name))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This email already exists"
		return render_template('register.html', error = error)
	else:
		cursor = conn.cursor()
		query = "SELECT * FROM Customer WHERE customerName = \'{}\'"
		cursor.execute(query.format(email, name))
		data = cursor.fetchone()
		cursor.close()
		if(data):
			#If the previous query returns data, then user exists
			error = "This username already exists"
			return render_template('register.html', error = error)

	ins = "INSERT INTO Customer(customerEmail, customerName, customerPassword) VALUES(\'{}\', \'{}\', \'{}\')"
	cursor = conn.cursor()
	cursor.execute(ins.format(email, name, password))
	conn.commit()
	cursor.close()
	flash("You are registered")
	return render_template('login.html', error= "Welcome! Please login~")




@app.route('/MainSquare', methods = ["GET"])
def MainSquare():
	cursor = conn.cursor()
	file = open("./Queries/post_item.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(itemName, itemProfile, itemDescription, auctionTime))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('mainSquare.html', posts=data1, error = error)

#------------------------------------login----------------------------------------

@app.route('/cus_login', methods=['POST', 'GET'])
def cus_login():
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM Customer WHERE username = \'{}\' and password = \'{}\'"
	cursor.execute(query.format(username, password))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
        login_user(username)
        MainSquare()
		#return render_template('mainSquare.html', type = "customer", name = username)	
	else:
		#returns an error message to the html page
		error = 'Invalid username or password'
		return render_template('login.html', error=error)
	error = 'Invalid username or password'
	return render_template('mainSquare.html', error=error)

@app.route('/Admin_login', methods=['POST'])
def Admin_login():
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM Admin WHERE adminName = \'{}\' and adminPassword = \'{}\'"
	cursor.execute(query.format(username, password, booking_agent_id))
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		login_user(username)
		print(username)
		return render_template('mainSquare.html', type = "admin", name = username)
	else:
		#returns an error message to the html page
		error = 'Invalid username or password'
		return render_template('login.html', error=error)







# #--------------------------customer-------------------------------------------

@app.route('/cus_search', methods = ["GET", "POST"])
def cus_search():
	keyword = request.form["keyword"]
	cursor = conn.cursor()
	file = open("./Queries/cus_search.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(keyword))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('mainSquare.html', posts=data1)



@app.route('/post_item', methods = ["GET", "POST"])
def post_item():
    itemName = request.form["itemName"]
    itemProfile = request.form["itemProfile"]
    itemDescription = request.form["itemDescription"]
    auctionTime = request.form["auctionTime"]

    cursor = conn.cursor()
    file = open("./Queries/post_item.sql","r")
    query = file.read()
    file.close()
    cursor.execute(query.format(itemName, itemProfile, itemDescription, auctionTime))
    cursor.close()
    error = "item posted!"
    MainSquare()
	# return render_template('mainSquare.html', posts=data1, error = error)







@app.route('/Product', methods = ["GET", "POST"])
def Product():
	productID = request.form["productID"]
	f = request.files['file']
	f.save()
	#f.save(secure_filename(f.filename))
	cursor = conn.cursor()
	file = open("./Queries/productInfo.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(itemName, itemProfile, itemDescription, auctionTime))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('Product.html', posts=data1, error = error)



@app.route('/myProduct', methods = ["GET"])
def myProduct():
	username = current_user.id
	cursor = conn.cursor()
	file = open("./Queries/myProduct.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('profile.html', posts=data1, error = error)



@app.route('/myTransaction', methods = ["GET"])
def myTransaction():
	username = current_user.id
	cursor = conn.cursor()
	file = open("./Queries/myTransaction.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('profile.html', posts=data1, error = error)


@app.route('/myProfile', methods = ["GET"])
def myProfile():
	username = current_user.id
	cursor = conn.cursor()
	file = open("./Queries/myProfile.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('profile.html', posts=data1, error = error)



@app.route('/verify', methods = ["GET"])
def myProfile():
	new_status = request.form["new_status"]
	cursor = conn.cursor()
	file = open("./Queries/myProfile.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('profile.html', posts=data1, error = error)

#-------------------------------------------------------------------------
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
