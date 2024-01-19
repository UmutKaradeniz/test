from flask import Blueprint, render_template, request, flash, redirect, url_for
from db_funcs import *
from flask_login import login_user, login_required, logout_user, current_user
from flask import session 

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
    
#function/route to login
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if DBfuncs.loginCustomerCheck(username, password) is not False:
            flash('Logged in as customer.', category = 'success')
            session['id'] = DBfuncs.getIDCustomer(username)
            return redirect(url_for('auth.customerhome'))
        elif DBfuncs.loginRestaurantCheck(username, password) is not False:
            flash('Logged in as restaurant', category = 'success')
            session['id'] = DBfuncs.getIDRestaurant(username)
            return redirect(url_for('auth.restauranthome'))
        else:
            flash('Please check your username and password', category = 'error')
    return render_template("login.html")

#function/route for custoerm home page
@auth.route('/customerhome', methods = ['GET', 'POST'])
def customerhome():
    if request.method == 'GET':
        if 'id' in session:
            id = session['id']
            restaurants = DBfuncs.retrieveResData(id)
            return render_template("customerhome.html", restaurants = restaurants)
        else:
            return redirect(url_for('auth.login'))
    return render_template("customerhome.html")

#function/route for custoerm home page
@auth.route('/restauranthome', methods = ['GET', 'POST'])
def restauranthome():
    if request.method == 'GET':
        if 'id' in session:
            id = session['id']
            menu_items = DBfuncs.retrieveMenuItems(id)
            return render_template("restauranthome.html", menu_items = menu_items)
        else:
            return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        item_id = request.form["btn"]
        print(item_id)
        return redirect(url_for('auth.edit_item', item_id = item_id))
        
#function/route for adding new item
@auth.route('/add_item', methods = ['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        if 'id' in session:
            id = session['id']
            name = request.form.get('itemname')
            description = request.form.get('itemdesc')
            type = request.form.get('itemtype')
            price = request.form.get('itemprice')
            DBfuncs.addNewItem(id, name, description, type, price)
            flash("Added new item successfully!")
            return redirect(url_for('auth.restauranthome'))
        else:
            return redirect(url_for('auth.login'))   
    return render_template("addmenuitem.html")

#function/route for adding new item
@auth.route('/edit_item', methods = ['GET', 'POST'])
def edit_item():
    if 'id' in session:
        item_id=request.args.get('item_id')
        print(item_id)
        menu_item = DBfuncs.retrieveMenuItem(item_id)
        if request.method == "POST":
            if request.form["btn"] == "save":
                name = request.form.get('itemname')
                description = request.form.get('itemdesc')
                type = request.form.get('itemtype')
                price = request.form.get('itemprice')
                DBfuncs.editItem(item_id, name, description, type, price)
                flash("Edited item successfully!")
                return redirect(url_for('auth.restauranthome'))
            elif request.form["btn"] == "remove":
                DBfuncs.deleteMenuItem(item_id)
                flash("Item removed successfully")
                return redirect(url_for('auth.restauranthome'))
        else:
            return render_template("editmenuitem.html", menu_item = menu_item)
    else:
        return redirect(url_for('auth.login'))   

@auth.route('/logout')
def logout():
    session.pop("id", None)
    return redirect(url_for('auth.login'))