from flask import Blueprint, render_template, request, flash, redirect, url_for
from db_funcs import *
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#function/route to render home page
@auth.route('/', methods = ['GET', 'POST'])
def homepage():
    return render_template("home.html")

#function/route to register customer
@auth.route('/signup', methods=['GET', 'POST'])
def registerCustomer():
    if request.method == 'POST':
        if request.form["btn"] == "customer":
            print(request.form)
            surname = request.form.get('surname')
            name = request.form.get('name')
            address = request.form.get('address')
            postcode = request.form.get('postcode')
            username = request.form.get('username')
            password = request.form.get('password')
            if surname == "" or name == "" or address == "" or len(postcode) != 5 or username == "" or password == "":
                flash('Please fill all of the entries of the form correctly.', category = 'error')
            elif DBfuncs.registerCustomer(surname, name, address, postcode, username, password) is not False:
                flash('Registration successful.', category = 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Username already exists. Please choose a different username.', category = 'error')

        if request.form["btn"] == "restaurant":            
            res_name = request.form.get('res_name')
            address = request.form.get('address')
            postcode = request.form.get('postcode')
            password = request.form.get('password')
            if res_name == "" or address == "" or len(postcode) != 5 or password == "":
                flash('Please fill all of the entries of the form correctly.', category = 'error')
            elif DBfuncs.registerRestaurant(res_name, address, postcode, password) is not False:
                flash('Registration successful.', category = 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Restaurant name already exists. Please choose a different username.', category = 'error')

    return render_template("sign-up.html")

#function/route to restaurant customer
# @auth.route('/signup_restaurant', methods=['GET', 'POST'])
# def registerRestaurant():
#     if request.method == 'POST':
#         res_name = request.form.get('res_name')
#         address = request.form.get('address')
#         postcode = request.form.get('postcode')
#         password = request.form.get('password')
#         if res_name == "" or address == "" or len(postcode) < 5 or password == "":
#             flash('Please fill all of the entries of the form correctly.', category = 'success')
#         elif DBfuncs.registerRestaurant(res_name, address, postcode, password) is not False:
#             flash('Registration successful.', category = 'success')
#             return render_template("login.html")
#         else:
#             flash('Restaurant name already exists. Please choose a different username.', category = 'error')
#     return render_template("sign-up.html")    
    

#function/route to login
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        global id
        if DBfuncs.loginCustomerCheck(username, password) is not False:
            flash('Logged in as customer.', category = 'success')
            # print(id)
            id = DBfuncs.getIDCustomer(username)
            # print(id)
            return redirect(url_for('auth.customerhome'))
        elif DBfuncs.loginRestaurantCheck(username, password) is not False:
            flash('Logged in as restaurant', category = 'success')
            id = DBfuncs.getIDRestaurant(username)
            # print(id)
            return render_template("customerhome.html")
        else:
            flash('Please check your username and password', category = 'error')
    return render_template("login.html")

@auth.route('/customerhome', methods = ['GET', 'POST'])
def customerhome():
    if request.method == 'GET':
        #print(id)
        restaurants = DBfuncs.retrieveResData(4)
        return render_template("customerhome.html", restaurants = restaurants)
    return render_template("customerhome.html")
        
@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))