from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from db_funcs import *
from flask import session 
from datetime import datetime
import os
import uuid

auth = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#function/route to render home page
@auth.route('/', methods = ['GET', 'POST'])
def homepage():
    return render_template("home.html")

#function/route to register customer
@auth.route('/signup', methods=['GET', 'POST'])
def registerCustomer():
    if request.method == 'POST':
        if request.form["btn"] == "customer":
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
        elif request.form["btn"] == "restaurant":          
            res_name = request.form.get('res_name')
            address = request.form.get('address')
            postcode = request.form.get('postcode')
            password = request.form.get('password')
            file = request.files['file']
            # if user does not select file, set filename to default picture
            if file.filename == '':
                filename = 'default-restaurant-picture.png'
            elif file and allowed_file(file.filename):
                file.filename = str(uuid.uuid4()) + ".png"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename).replace("\\", "/"))
                filename = file.filename
            if res_name == "" or address == "" or len(postcode) != 5 or password == "":
                flash('Please fill all of the entries of the form correctly.', category = 'error')
            elif DBfuncs.registerRestaurant(res_name, address, postcode, password, filename) is not False:
                flash('Registration successful.', category = 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Restaurant name already exists. Please choose a different username.', category = 'error')

    return render_template("sign-up.html")  

def allowed_file(filename): return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   

#function/route to login
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if DBfuncs.loginCustomerCheck(username, password) is not False:
            flash('Logged in as customer.', category = 'success')
            session['id'] = (DBfuncs.getIDCustomer(username))
            session['cart'] = []
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
    if 'id' in session:
        if request.method == 'GET':
            cus_id = session['id']
            restaurants = DBfuncs.retrieveResData(cus_id)
            print(restaurants)
            return render_template("customerhome.html", restaurants = restaurants)
        if request.method == 'POST':
            res_id = request.form["btn"]
            if len(session['cart']) != 0:
                if session['cart'][0] == res_id:
                    pass
                else:
                    session.pop("cart", default = None)
                    flash("Shopping cart has been reset.", category = 'error')
                    session['cart'] = []
                    session['cart'].append(res_id)
                    session.modified = True
            else:
                session['cart'].append(res_id)
                session.modified = True
            return redirect(url_for('auth.menu', res_id = res_id))
    else:
        return redirect(url_for('auth.login'))
    
@auth.route('/menu', methods = ['GET', 'POST'])
def menu():
    if 'id' in session:
        res_id = request.args.get('res_id')
        menu_items = DBfuncs.retrieveMenuItems(res_id)
        if request.method == 'POST':
            item_id = request.form["btn"]
            if item_id in session['cart'][1:]:
                flash("This item is already in shopping cart. In order to change quantity please go tou your shopping cart.", category = "error")
                return render_template("orderfood.html", menu_items = menu_items)
            else:
                session['cart'].append(item_id)
                session.modified = True
                flash("Item Added to the Cart", category = 'success')
                return render_template("orderfood.html", menu_items = menu_items)
        else:
            return render_template("orderfood.html", menu_items = menu_items)
    else:
        return redirect(url_for('auth.login'))
    
@auth.route('/shopping_cart', methods = ['GET', 'POST'])
def shopping_cart():
    if 'id' in session:
        menu_items= []
        cus_id = session['id']
        for item_id in session['cart'][1:]:
            menu_items.append(DBfuncs.retrieveMenuItem(item_id))
        user_info = DBfuncs.retrieveCusData(cus_id)
        if request.method == 'POST':
            if request.form["btn"] == "confirm":
                order = ""
                i = 0
                time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                res_id = session['cart'][0]
                res_name = DBfuncs.getResName(res_id)
                cus_name, cus_surname, cus_address = DBfuncs.getCusNameAddress(cus_id)
                for key, value in request.form.items():
                    if "quantity" in key:
                        order = order + str(menu_items[i][1]) + ' x' + str(value) + "\n"
                        i = i + 1
                    if "comment" in key:
                        comment = value
                DBfuncs.addNewOrder(time, res_id, res_name, cus_id, cus_name, cus_surname, cus_address, order, comment)
                return redirect(url_for('auth.order_list'))
            elif request.form["btn"] in session['cart'][1:]:
                item_id = request.form["btn"]
                session['cart'][1:] = [ele for ele in session['cart'][1:] if ele != item_id]
                session.modified = True
                return redirect(url_for('auth.shopping_cart'))
        else:
            return render_template("shoppingcart.html", menu_items = menu_items, user_info = user_info)
    else:
        return redirect(url_for('auth.login'))

@auth.route('/order_list', methods = ['GET', 'POST'])
def order_list():
    if 'id' in session:
        cus_id = session['id']
        orders = DBfuncs.getCustomerOrders(cus_id)
        return render_template("customerorders.html", orders = orders)
    else:
        return redirect(url_for('auth.login'))

#function/route for custoerm home page
@auth.route('/restauranthome', methods = ['GET', 'POST'])
def restauranthome():
    if 'id' in session:
        if request.method == 'GET':
            id = session['id']
            menu_items = DBfuncs.retrieveMenuItems(id)
            return render_template("restauranthome.html", menu_items = menu_items)
        if request.method == 'POST':
            item_id = request.form["btn"]
            return redirect(url_for('auth.edit_item', item_id = item_id))
    else:
        return redirect(url_for('auth.login'))
        
#function/route for adding new item
@auth.route('/add_item', methods = ['GET', 'POST'])
def add_item():
    if 'id' in session:
        if request.method == 'POST':
            id = session['id']
            name = request.form.get('itemname')
            description = request.form.get('itemdesc')
            type = request.form.get('itemtype')
            price = request.form.get('itemprice')
            file = request.files['file']
            if file.filename == '':
                filename = type + ".png"
            elif file and allowed_file(file.filename):
                file.filename = str(uuid.uuid4()) + ".png"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename).replace("\\", "/"))
                filename = file.filename
            DBfuncs.addNewItem(id, name, description, type, price, filename)
            flash("Added new item successfully!", category = 'success')
            return redirect(url_for('auth.restauranthome'))
        else:  
            return render_template("addmenuitem.html")
    else:
        return redirect(url_for('auth.login')) 
    
#function/route for adding new item
@auth.route('/edit_item', methods = ['GET', 'POST'])
def edit_item():
    if 'id' in session:
        item_id=request.args.get('item_id')
        menu_item = DBfuncs.retrieveMenuItem(item_id)
        if request.method == "POST":
            if request.form["btn"] == "save":
                name = request.form.get('itemname')
                description = request.form.get('itemdesc')
                type = request.form.get('itemtype')
                price = request.form.get('itemprice')
                file = request.files['file']
                if file.filename == '':
                    filename = DBfuncs.retrieveFileName(item_id)
                elif file and allowed_file(file.filename):
                    if file.name is not 'default-food-picture.png':
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], DBfuncs.retrieveFileName(item_id)))
                    file.filename = str(uuid.uuid4()) + ".png"
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
                    filename = file.filename
                DBfuncs.editItem(item_id, name, description, type, price, filename)
                flash("Edited item successfully!" , category = 'success')
                return redirect(url_for('auth.restauranthome'))
            elif request.form["btn"] == "remove":
                DBfuncs.deleteMenuItem(item_id)
                flash("Item removed successfully" , category = 'error')
                return redirect(url_for('auth.restauranthome'))
        else:
            return render_template("editmenuitem.html", menu_item = menu_item)
    else:
        return redirect(url_for('auth.login'))   
    
@auth.route('/settings', methods = ['GET', 'POST'])
def settings():
    if 'id' in session:
        id = session['id']
        plzList = DBfuncs.getPlzList(id)
        if request.method == "POST":
            if request.form["btn"] == "save":
                hour_open = request.form.get('hour1')
                minute_open = request.form.get('min1')
                hour_close = request.form.get('hour2')
                minute_close = request.form.get('min2')
                if hour_open > hour_close:
                    flash("Opening hour cannot be later than Closing hour" , category = 'error')
                    return redirect(url_for('auth.settings'))
                else:
                    open_time = hour_open + ':' + minute_open
                    close_time = hour_close + ':' + minute_close
                    DBfuncs.setTime(id, open_time, close_time)
                    flash("Time set successfully" , category = 'success')
                    return redirect(url_for('auth.settings'))
            elif request.form["btn"] == "plz":
                plz = request.form.get('integerInput')
                if DBfuncs.addNewPostcode(id, plz) is not False and len(plz) == 5:
                    flash("Postcode added successfully" , category = 'success')
                    return redirect(url_for('auth.settings'))
                else:
                    flash("This postcode already exists", category = "error")
                    return redirect(url_for('auth.settings'))
        else:
            return render_template("restaurantsettings.html", plzList = plzList)
    else:
        return redirect(url_for('auth.login'))
    
@auth.route('/orders', methods = ['GET', 'POST'])
def orders():
    if 'id' in session:
        res_id = session['id']
        orders = DBfuncs.getRestaurantOrders(res_id)
        if request.method == 'POST':
            if 'confirm' in request.form.keys():
                ord_id = request.form["confirm"]
                DBfuncs.changeStatusOrder("in preparation", ord_id)
            elif 'cancel' in request.form.keys():
                ord_id = request.form["cancel"]
                DBfuncs.changeStatusOrder("cancelled", ord_id)
            elif 'complete' in request.form.keys():
                ord_id = request.form["complete"]
                DBfuncs.changeStatusOrder("completed", ord_id)
            return redirect(url_for('auth.orders'))
        return render_template("restaurantorders.html", orders = orders)
    else:
        return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.pop("id", default = None)
    session.pop("cart", default = None)
    return redirect(url_for('auth.login'))