from flask import Blueprint, render_template, request, jsonify, flash
from db_funcs import *

auth = Blueprint('auth', __name__)

#function/route to render home page
@auth.route('/', methods = ['GET', 'POST'])
def homepage():
    return render_template("home.html")

#function/route to register customer
@auth.route('/register_customer', methods=['GET', 'POST'])
def registerCustomer():
    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        address = request.form.get('address')
        postcode = request.form.get('postcode')
        username = request.form.get('username')
        password = request.form.get('password')
        if DBfuncs.registerCustomer(surname, name, address, postcode, username, password) is not False:
            flash('Registration successful.', category = 'success')
        else:
            flash('Username already exists. Please choose a different username.', category = 'error')
    
    return render_template("sign-up.html")

#function/route to restaurant customer
@auth.route('/register_restaurant', methods=['GET', 'POST'])
def registerRestaurant():
    if request.method == 'POST':
        res_name = request.form.get('res_name')
        address = request.form.get('address')
        postcode = request.form.get('postcode')
        password = request.form.get('password')
        if DBfuncs.registerRestaurant(res_name, address, postcode, password) is not False:
            flash('Registration successful.', category = 'success')
        else:
            flash('Restaurant name already exists. Please choose a different username.', category = 'error')
        
    return render_template("sign-up.html")