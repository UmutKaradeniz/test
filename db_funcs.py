import sqlite3 as sql
from datetime import datetime

class DBfuncs:
    #Creating every table that is needed in our website's backend
    def createTables():
        con = sql.connect('database.db')
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY autoincrement,
                surname TEXT NOT NULL,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                postcode INTEGER NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL                      
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                res_name TEXT UNIQUE NOT NULL,
                address TEXT NOT NULL,
                postcode INTEGER NOT NULL,
                password TEXT NOT NULL,
                picture BLOB,
                opening TIME,
                closing TIME                          
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS menu_items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                res_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL, 
                type TEXT CHECK(TYPE IN('Main', 'Side', 'Dessert', 'Drink')) NOT NULL,
                price INTEGER NOT NULL,
                FOREIGN KEY(res_id) REFERENCES restaurants(id)       
            )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS allowed_postcode(
                res_id INTEGER NOT NULL,
                postcode INTEGER NOT NULL,  
                FOREIGN KEY(res_id) REFERENCES restaurants(id)               
            )""")
        con.commit()
        con.close()

    #Customer registration to the DB
    def registerCustomer(surname, name, address, postcode, username, password):
        con = sql.connect('database.db')
        cur = con.cursor()
        response = False
        cur.execute("SELECT EXISTS (SELECT * FROM customers WHERE username=?)", (username,))
        result = cur.fetchone()[0]
        if not bool(result):
            cur.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?)", (None, surname, name, address, postcode, username, password))
            response = True
        con.commit()
        con.close()
        return response

    #Restaurant registration to the DB
    def registerRestaurant(res_name, address, postcode, password, img_path = None):
        con = sql.connect('database.db')
        cur = con.cursor()
        response = False
        sqlite_insert_blob_query = """ INSERT INTO restaurants
                                  (id, res_name, address, postcode, password, picture) VALUES (?, ?, ?, ?, ?, ?)"""
        data_tuple = (None, res_name, address, postcode, password, img_path)
        cur.execute("SELECT EXISTS (SELECT * FROM restaurants WHERE res_name=?)", (res_name,))
        result = cur.fetchone()[0]
        if not bool(result):
            cur.execute(sqlite_insert_blob_query, data_tuple)
            response = True
        con.commit()
        con.close()
        return response

    #Credentials check for customer login
    def loginCustomerCheck(username, password):
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM customers WHERE username=? AND password=?)", (username, password))
        result = cur.fetchone()[0]
        con.close()
        return True if bool(result) == True else False
    
    #Credentials check for restaurant login
    def loginRestaurantCheck(res_name, password):
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM restaurants WHERE res_name=? AND password=?)", (res_name, password))
        result = cur.fetchone()[0]  
        con.close()
        return True if bool(result) == True else False  
    
    #Adding menu item to Restaurant Menu
    def addNewItem(res_id, name, ingredients, type, price):
        try:
            con = sql.connect('database.db')
            con.execute("PRAGMA foreign_keys = ON")
            cur = con.cursor() 
            cur.execute("INSERT INTO menu_items VALUES (?, ?, ?, ?, ?, ?)", (None, res_id, name, ingredients, type, price))
            con.commit()
            con.close()
            return True
        except sql.Error as Err:
            print("SQLite Error: ", Err)
            return False
        
    #Editing menu item frım Restaurant Menu
    def editItem(item_id, name, ingredients, type, price):
        try:
            con = sql.connect('database.db')
            con.execute("PRAGMA foreign_keys = ON")
            cur = con.cursor() 
            cur.execute("""UPDATE menu_items SET name = (?), ingredients = (?),
                        type = (?), price = (?) WHERE id= (?)""", (name, ingredients, type, price, item_id))
            con.commit()
            con.close()
        except sql.Error as Err:
            print("SQLite Error: ", Err)

    #Finding menu item ID
    def getItemID(res_id, name):
        con = sql.connect('database.db')
        cur = con.cursor() 
        cur.execute("SELECT id FROM menu_items WHERE res_id = (?) and name = (?)", (res_id, name))
        data = cur.fetchone()[0]
        con.commit()
        con.close()
        return data
    
    #returns id from the row of the given username
    def getIDRestaurant(username):
        con = sql.connect('database.db')
        cur = con.cursor() 
        cur.execute("SELECT id FROM restaurants WHERE res_name=?", (username, ))
        id = cur.fetchone()[0]
        return id
    
    def getIDCustomer(username):
        con = sql.connect('database.db')
        cur = con.cursor() 
        cur.execute("SELECT id FROM customers WHERE username=?", (username, ))
        id = cur.fetchone()[0]
        return id
    
    def addNewPostcode(res_id, postcode):
        try:
            con = sql.connect('database.db')
            con.execute("PRAGMA foreign_keys = ON")
            cur = con.cursor() 
            response = False
            cur.execute("SELECT EXISTS (SELECT 1 FROM allowed_postcode WHERE res_id = (?) and postcode = (?)) ", (res_id, postcode))
            result = cur.fetchone()[0]
            if not bool(result):
                cur.execute("INSERT INTO allowed_postcode VALUES (?, ?)", (res_id, postcode))     
                response = True   
            con.commit()
            con.close()
            return response
        except sql.Error as Err:
            print("SQLite Error: ", Err)
            return False 
        
    def retrieveResData(id):
        con = sql.connect('database.db')
        cur = con.cursor()
        current = datetime.now().strftime('%H:%M')
        cur.execute("SELECT opening, closing FROM restaurants WHERE id=?", (id,))
        result = cur.fetchone()
        opening, closing = result
        if opening or closing: 
            status = DBfuncs.is_open(current, opening, closing)
        else:
            status = "CLOSED"
        cur.execute("""SELECT id, res_name, address, postcode, opening, closing, ? as status FROM restaurants WHERE id IN 
                    (SELECT res_id FROM allowed_postcode WHERE postcode IN (SELECT postcode FROM customers WHERE id = ?))""", (status, id))
        data = cur.fetchall()
        con.commit()
        con.close()
        return data
    
    def is_open(current, opening, closing):
        return "OPEN" if opening <= current <= closing else "CLOSED"
    
    def retrieveMenuItems(id):
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("""SELECT id, name, ingredients, type, price FROM menu_items
                        WHERE res_id = ?""", (id, ))
        data = cur.fetchall()
        print(data)
        con.commit()
        con.close()
        return data
    
    def retrieveMenuItem(item_id):
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("""SELECT id, name, ingredients, type, price FROM menu_items
                        WHERE id = ?""", (item_id, ))
        data = cur.fetchone()
        con.commit()
        con.close()
        return data
    
    def deleteMenuItem(item_id):
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("DELETE FROM menu_items WHERE id =?", (item_id, ))
        con.commit()
        con.close()

    def setTime(restaurant_id, open_time, close_time):
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("UPDATE restaurants SET opening = ?, closing = ? WHERE id = ?", (open_time, close_time, restaurant_id))
        con.commit()
        con.close()

    def getPlzList(res_id):
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT postcode FROM allowed_postcode WHERE res_id = (?)", (res_id, ))
        data = cur.fetchall()
        con.commit()
        con.close()
        return data
    
if __name__ == "__main__":
    DBfuncs.createTables()
    # DBfuncs.registerCustomer("Karadeniz2", "Umut", "ABC 6", 47055, "Umut_Karadeniz", 1234554321)
    # DBfuncs.registerRestaurant("Al-Basha2", "ABC 7", 47055, 123321)
    # DBfuncs.addNewItem(3, "hamburger", "meat", "Main", 20)
    # DBfuncs.addNewPostcode(1, 12345)
    # DBfuncs.addNewPostcode(2, 12345)
    # DBfuncs.addNewPostcode(3, 12345)
    # DBfuncs.addNewPostcode(1, 23456)
    # DBfuncs.addNewPostcode(2, 23456)
    # DBfuncs.retrieveResData(4)
    # DBfuncs.retrieveResData(3)
    # DBfuncs.getIDCustomer("a")
    # DBfuncs.addNewItem(5, "pizza", "tomato", "Main", 15)
    # DBfuncs.addNewItem(5, "hamburger", "meat", "Main", 25)
    # DBfuncs.addNewItem(5, "ice-cream", "vanilla", "Desert", 5)
    # DBfuncs.retrieveMenuItems(5)