from db_funcs import *

def initExampleDB():
    customers = [
        ('Smith', 'John', '123 Main St', 12345, 'jsmith', 'password123'),
        ('Johnson', 'Alice', '456 Oak St', 56789, 'ajohnson', 'securepass'),
        ('Davis', 'Michael', '789 Pine St', 98765, 'mdavis', 'mypassword'),
        ('Miller', 'Sarah', '101 Elm St', 54321, 'smiller', 'letmein123'),
        ('Wilson', 'David', '202 Maple St', 13579, 'dwilson', 'pass123')
    ]
    restaurants = [
        ('Bella Italia', '123 Main St', 12345, 'password123', '08:00:00', '22:00:00'),
        ('Taste of India', '456 Oak St', 56789, 'securepass', '11:30:00', '20:30:00'),
        ('Mamma Mia Pizzeria', '789 Pine St', 98765, 'mypassword', '10:00:00', '23:00:00'),
        ('Sushi Heaven', '101 Elm St', 54321, 'letmein123', '12:00:00', '21:00:00'),
        ('Steakhouse Deluxe', '202 Maple St', 13579, 'pass123', '17:00:00', '23:30:00'),
        ('Vegetarian Delights', '303 Birch St', 24680, 'password456', '09:00:00', '20:00:00'),
        ('The Burger Joint', '404 Cedar St', 87654, 'secure123', '11:00:00', '22:30:00'),
        ('Seafood Sensation', '505 Walnut St', 23456, 'mypassword789', '12:30:00', '21:30:00'),
        ('Mexican Fiesta', '606 Oakwood St', 78901, 'password789', '10:30:00', '22:00:00'),
        ('Noodle House', '707 Pinecrest St', 32145, 'letmein456', '11:00:00', '20:00:00'),
        ('BBQ Grill Masters', '808 Cedarwood St', 56789, 'secure456', '15:00:00', '23:00:00')
    ]
    menu_items = [
        # Menu items for Bella Italia (res_id = 1)
        (1, 'Margherita Pizza', 'Tomato, Mozzarella, Basil', 'Main', 12),
        (1, 'Spaghetti Bolognese', 'Beef Bolognese Sauce', 'Main', 15),
        (1, 'Tiramisu', 'Ladyfingers, Coffee, Mascarpone', 'Dessert', 8),
        (1, 'Minestrone Soup', 'Vegetables, Pasta, Broth', 'Side', 6),
        (1, 'Espresso', 'High-Quality Coffee', 'Drink', 4),
        (1, 'Calzone', 'Ham, Ricotta, Mushrooms', 'Main', 14),
        (1, 'Caprese Side', 'Tomato, Mozzarella, Basil', 'Side', 9),
        (1, 'Seafood Risotto', 'Arborio Rice, Seafood Mix', 'Main', 18),
        (1, 'Panna Cotta', 'Cream, Sugar, Vanilla', 'Dessert', 10),
        (1, 'Limoncello', 'Italian Lemon Liqueur', 'Drink', 7),

        # Menu items for Taste of India (res_id = 2)
        (2, 'Chicken Tikka Masala', 'Chicken, Tomato Sauce, Spices', 'Main', 16),
        (2, 'Vegetable Biryani', 'Basmati Rice, Mixed Vegetables', 'Main', 14),
        (2, 'Naan Bread', 'Flour, Yogurt, Baking Powder', 'Side', 5),
        (2, 'Mango Lassi', 'Yogurt, Mango, Sugar', 'Drink', 4),
        (2, 'Samosa', 'Potato, Peas, Spices', 'Side', 6),
        (2, 'Gulab Jamun', 'Milk Powder, Sugar, Ghee', 'Dessert', 8),
        (2, 'Chicken Korma', 'Chicken, Coconut, Cashews', 'Main', 17),
        (2, 'Paneer Tikka', 'Paneer, Spices, Yogurt', 'Main', 13),
        (2, 'Raita', 'Yogurt, Cucumber, Mint', 'Side', 4),
        (2, 'Chai Tea', 'Tea, Milk, Spices', 'Drink', 3),

        # Menu items for Mamma Mia Pizzeria (res_id = 3)
        (3, 'Pepperoni Pizza', 'Pepperoni, Tomato Sauce, Mozzarella', 'Main', 13),
        (3, 'Pasta Carbonara', 'Pasta, Pancetta, Egg, Parmesan', 'Main', 14),
        (3, 'Garlic Bread', 'Baguette, Garlic, Butter', 'Side', 6),
        (3, 'Chocolate Cannoli', 'Ricotta, Chocolate Chips, Pastry', 'Dessert', 9),
        (3, 'Antipasto Platter', 'Salami, Prosciutto, Cheese', 'Side', 12),
        (3, 'Vegetarian Pizza', 'Tomato Sauce, Mozzarella, Mixed Vegetables', 'Main', 12),
        (3, 'Caesar Side', 'Romaine Lettuce, Croutons, Caesar Dressing', 'Side', 8),
        (3, 'Calamari Fritti', 'Squid, Flour, Lemon', 'Main', 15),
        (3, 'Cannoli Siciliani', 'Ricotta, Candied Fruit, Pastry', 'Dessert', 10),
        (3, 'Italian Soda', 'Soda, Syrup, Ice', 'Drink', 4),

        # Menu items for Sushi Heaven (res_id = 4)
        (4, 'Sashimi Platter', 'Assorted Raw Fish', 'Main', 20),
        (4, 'Dragon Roll', 'Shrimp Tempura, Avocado, Eel Sauce', 'Main', 18),
        (4, 'Miso Soup', 'Tofu, Seaweed, Broth', 'Side', 5),
        (4, 'Edamame', 'Steamed Soybeans, Salt', 'Side', 4),
        (4, 'Rainbow Roll', 'Assorted Fish, Avocado, Rice', 'Main', 16),
        (4, 'Tempura Udon', 'Udon Noodles, Tempura, Broth', 'Main', 14),
        (4, 'California Roll', 'Avocado, Crab, Cucumber', 'Main', 15),
        (4, 'Green Tea Ice Cream', 'Green Tea, Cream, Sugar', 'Dessert', 7),
        (4, 'Spicy Tuna Roll', 'Tuna, Spicy Mayo, Cucumber', 'Main', 17),
        (4, 'Sake', 'Japanese Rice Wine', 'Drink', 8),

        # Menu items for Steakhouse Deluxe (res_id = 5)
        (5, 'Filet Mignon', 'Beef Tenderloin', 'Main', 32),
        (5, 'Ribeye Steak', 'Ribeye Cut, Marbling', 'Main', 28),
        (5, 'Loaded Baked Potato', 'Potato, Cheese, Bacon', 'Side', 8),
        (5, 'Caesar Side', 'Romaine Lettuce, Croutons, Parmesan', 'Side', 10),
        (5, 'Grilled Asparagus', 'Asparagus, Olive Oil, Salt', 'Side', 9),
        (5, 'New York Strip', 'Striploin Cut, Seasonings', 'Main', 30),
        (5, 'Garlic Butter Shrimp', 'Shrimp, Garlic, Butter', 'Main', 24),
        (5, 'Mashed Potatoes', 'Potatoes, Cream, Butter', 'Side', 7),
        (5, 'Chocolate Lava Cake', 'Chocolate, Flour, Eggs', 'Dessert', 12),
        (5, 'Old Fashioned', 'Bourbon, Sugar, Bitters', 'Drink', 10),

        # Menu items for Vegetarian Delights (res_id = 6)
        (6, 'Quinoa Side', 'Quinoa, Mixed Vegetables, Balsamic Dressing', 'Main', 14),
        (6, 'Eggplant Parmesan', 'Eggplant, Tomato Sauce, Mozzarella', 'Main', 16),
        (6, 'Hummus Platter', 'Chickpeas, Tahini, Pita Bread', 'Side', 8),
        (6, 'Stuffed Bell Peppers', 'Bell Peppers, Rice, Beans', 'Main', 15),
        (6, 'Vegan Chocolate Cake', 'Flour, Cocoa Powder, Almond Milk', 'Dessert', 10),
        (6, 'Spinach and Artichoke Dip', 'Spinach, Artichoke, Cream Cheese', 'Side', 9),
        (6, 'Vegetable Stir Fry', 'Mixed Vegetables, Soy Sauce, Rice', 'Main', 13),
        (6, 'Cauliflower Wings', 'Cauliflower, Buffalo Sauce, Ranch', 'Side', 11),
        (6, 'Chia Seed Pudding', 'Chia Seeds, Almond Milk, Berries', 'Dessert', 7),
        (6, 'Berry Smoothie', 'Berries, Yogurt, Honey', 'Drink', 6),

        # Menu items for The Burger Joint (res_id = 7)
        (7, 'Classic Cheeseburger', 'Beef Patty, Cheese, Lettuce, Tomato', 'Main', 10),
        (7, 'Crispy Chicken Sandwich', 'Chicken Breast, Lettuce, Mayo', 'Main', 12),
        (7, 'Onion Rings', 'Onions, Batter, Deep Fried', 'Side', 6),
        (7, 'Sweet Potato Fries', 'Sweet Potatoes, Olive Oil, Salt', 'Side', 7),
        (7, 'BBQ Bacon Burger', 'Beef Patty, Bacon, BBQ Sauce', 'Main', 13),
        (7, 'Veggie Burger', 'Black Bean Patty, Avocado, Salsa', 'Main', 11),
        (7, 'Mozzarella Sticks', 'Mozzarella, Breadcrumbs, Marinara Sauce', 'Side', 8),
        (7, 'Chili Cheese Fries', 'French Fries, Chili, Cheese', 'Side', 9),
        (7, 'Chocolate Shake', 'Ice Cream, Milk, Chocolate Syrup', 'Drink', 5),
        (7, 'Iced Tea', 'Tea, Ice, Lemon', 'Drink', 3),

        # Menu items for Seafood Sensation (res_id = 8)
        (8, 'Lobster Bisque', 'Lobster, Cream, Sherry', 'Side', 15),
        (8, 'Grilled Salmon', 'Salmon, Lemon, Dill', 'Main', 22),
        (8, 'Shrimp Scampi', 'Shrimp, Garlic, Butter', 'Main', 18),
        (8, 'Clam Chowder', 'Clams, Potatoes, Bacon', 'Side', 12),
        (8, 'Fish and Chips', 'Cod, Fries, Tartar Sauce', 'Main', 16),
        (8, 'Crab Cakes', 'Crab, Bread Crumbs, Mayo', 'Main', 20),
        (8, 'Seafood Paella', 'Shrimp, Mussels, Rice', 'Main', 25),
        (8, 'Ceviche', 'White Fish, Citrus Juice, Avocado', 'Side', 14),
        (8, 'Oyster Rockefeller', 'Oysters, Spinach, Pernod', 'Side', 16),
        (8, 'Mango Mojito', 'Rum, Mint, Mango', 'Drink', 8),

        # Menu items for Mexican Fiesta (res_id = 9)
        (9, 'Tacos al Pastor', 'Marinated Pork, Pineapple, Onion', 'Main', 10),
        (9, 'Guacamole', 'Avocado, Tomato, Onion', 'Side', 8),
        (9, 'Chicken Enchiladas', 'Chicken, Cheese, Enchilada Sauce', 'Main', 12),
        (9, 'Chiles Rellenos', 'Poblano Peppers, Cheese, Tomato Sauce', 'Main', 14),
        (9, 'Quesadillas', 'Cheese, Tortilla, Salsa', 'Main', 9),
        (9, 'Salsa and Chips', 'Tomato, Onion, Cilantro', 'Side', 6),
        (9, 'Burrito Bowl', 'Rice, Black Beans, Fajita Veggies', 'Main', 11),
        (9, 'Horchata', 'Rice Milk, Cinnamon, Vanilla', 'Drink', 4),
        (9, 'Flan', 'Caramel, Eggs, Condensed Milk', 'Dessert', 7),
        (9, 'Margarita', 'Tequila, Triple Sec, Lime', 'Drink', 8),

        # Menu items for Noodle House (res_id = 10)
        (10, 'Pad Thai', 'Rice Noodles, Shrimp, Tofu', 'Main', 12),
        (10, 'Beef Pho', 'Rice Noodles, Beef Broth, Basil', 'Main', 14),
        (10, 'Vegetable Spring Rolls', 'Rice Paper, Veggies, Peanut Sauce', 'Side', 8),
        (10, 'Chicken Teriyaki Bowl', 'Grilled Chicken, Teriyaki Sauce, Rice', 'Main', 11),
        (10, 'Sushi Burrito', 'Sushi Rice, Salmon, Avocado', 'Main', 13),
        (10, 'Miso Ramen', 'Ramen Noodles, Miso Broth, Seaweed', 'Main', 10),
        (10, 'Edamame Beans', 'Steamed Soybeans, Salt', 'Side', 5),
        (10, 'Matcha Green Tea Ice Cream', 'Matcha, Cream, Sugar', 'Dessert', 9),
        (10, 'Drunken Noodles', 'Wide Rice Noodles, Chicken, Basil', 'Main', 15),
        (10, 'Bubble Tea', 'Black Tea, Milk, Tapioca Pearls', 'Drink', 6),

        # Menu items for BBQ Grill Masters (res_id = 11)
        (11, 'Brisket Plate', 'Smoked Brisket, BBQ Sauce, Coleslaw', 'Main', 18),
        (11, 'Pulled Pork Sandwich', 'Pulled Pork, BBQ Sauce, Pickles', 'Main', 15),
        (11, 'Mac and Cheese', 'Elbow Macaroni, Cheese Sauce, Bread Crumbs', 'Side', 8),
        (11, 'Baby Back Ribs', 'Baby Back Pork Ribs, Dry Rub, BBQ Glaze', 'Main', 20),
        (11, 'Burnt Ends', 'Smoked Beef Ends, BBQ Sauce', 'Main', 16),
        (11, 'Cornbread', 'Cornmeal, Flour, Buttermilk', 'Side', 6),
        (11, 'BBQ Chicken Wings', 'Chicken Wings, BBQ Seasoning', 'Side', 10),
        (11, 'Collard Greens', 'Collard Greens, Bacon, Onion', 'Side', 7),
        (11, 'Peach Cobbler', 'Peaches, Sugar, Cinnamon', 'Dessert', 9),
        (11, 'Sweet Tea', 'Black Tea, Sugar, Lemon', 'Drink', 4)
    ]
    
    restaurant_postcodes = [
        # Postcodes for Bella Italia (res_id = 1)
        (1, 12345),
        (1, 56789),
        (1, 98765),
        (1, 12348),
        (1, 12349),
        (1, 12350),
        (1, 12351),
        (1, 12352),
        (1, 54321),
        (1, 12354),

        # Postcodes for Taste of India (res_id = 2)
        (2, 12345),
        (2, 56789),
        (2, 56791),
        (2, 56792),
        (2, 98765),
        (2, 56794),
        (2, 56795),
        (2, 56796),
        (2, 56797),
        (2, 56798),

        # Postcodes for Mamma Mia Pizzeria (res_id = 3)
        (3, 12345),
        (3, 56789),
        (3, 98767),
        (3, 98768),
        (3, 98769),
        (3, 98770),
        (3, 98771),
        (3, 13579),
        (3, 98773),
        (3, 54321),

        # Postcodes for Sushi Heaven (res_id = 4)
        (4, 12345),
        (4, 56789),
        (4, 54323),
        (4, 54324),
        (4, 54325),
        (4, 54326),
        (4, 54327),
        (4, 13579),
        (4, 54329),
        (4, 54330),

        # Postcodes for Steakhouse Deluxe (res_id = 5)
        (5, 13579),
        (5, 13580),
        (5, 13581),
        (5, 13582),
        (5, 98765),
        (5, 13584),
        (5, 13585),
        (5, 13579),
        (5, 13587),
        (5, 54321),

        # Postcodes for Vegetarian Delights (res_id = 6)
        (6, 12345),
        (6, 56789),
        (6, 24682),
        (6, 24683),
        (6, 24684),
        (6, 24685),
        (6, 24686),
        (6, 13579),
        (6, 24688),
        (6, 24689),

        # Postcodes for The Burger Joint (res_id = 7)
        (7, 11111),
        (7, 11112),
        (7, 11113),
        (7, 11114),
        (7, 11115),
        (7, 13579),
        (7, 11117),
        (7, 98765),
        (7, 11119),
        (7, 54321),

        # Postcodes for Seafood Sensation (res_id = 8)
        (8, 22222),
        (8, 22223),
        (8, 22224),
        (8, 22225),
        (8, 22226),
        (8, 22227),
        (8, 22228),
        (8, 13579),
        (8, 22230),
        (8, 22231),

        # Postcodes for Mexican Fiesta (res_id = 9)
        (9, 33333),
        (9, 33334),
        (9, 33335),
        (9, 33336),
        (9, 33337),
        (9, 33338),
        (9, 33339),
        (9, 13579),
        (9, 33341),
        (9, 54321),

        # Postcodes for Noodle House (res_id = 10)
        (10, 44444),
        (10, 44445),
        (10, 44446),
        (10, 44447),
        (10, 44448),
        (10, 44449),
        (10, 44450),
        (10, 44451),
        (10, 44452),
        (10, 44453),

        # Postcodes for BBQ Grill Masters (res_id = 11)
        (11, 55555),
        (11, 55556),
        (11, 55557),
        (11, 98765),
        (11, 55559),
        (11, 55560),
        (11, 55561),
        (11, 55562),
        (11, 55563),
        (11, 54321)
]
    
    orders = [
        # Order 1 for John
        ("2024-01-22 20:30", 1,'Bella Italia', 1, "John", "Smith", "123 Main St", 'Margherita Pizza x1\nLimoncello x1\n', "call dont ring"),

        # Order 2 for John
        ("2024-01-23 19:45", 2, 'Taste of India',1, "John", "Smith", "123 Main St", 'Chicken Tikka Masala x4\nVegetable Biryani x2\n', "make it a bit spicy"),

        # Order 1 for Alice
        ("2024-01-24 18:15", 5, 'Steakhouse Deluxe',2, "Alice", "Johnson", "456 Oak St", 'Filet Mignon x2\nOld Fashioned x3\n', "hello examinor"),

        # Order 2 for Alice
        ("2024-01-25 20:00", 2, 'Taste of India',2, "Alice", "Johnson", "456 Oak St", 'Chicken Korma x4\nGulab Jamun x1\n', "this is an example comment"),

        # Order 1 for Michael
        ("2024-01-22 17:30", 3, 'Mamma Mia Pizzeria',3, "Michael", "Davis", "789 Pine St", 'Chocolate Cannoli x3\nAntipasto Platter x3\n', "Lorem ipsum dolor sit amet"),

        # Order 2 for Michael
        ("2024-01-23 18:45", 3, 'Mamma Mia Pizzeria',3, "Michael", "Davis", "789 Pine St", 'Caesar Side x1\nCalamari Fritti x1\n', "Duis at mi fringilla"),

        # Order 1 for Sarah
        ("2024-01-24 18:15", 5, 'Steakhouse Deluxe',4, "Sarah", "Miller", "101 Elm St", 'Grilled Asparagus x7\n', "ante ipsum primis"),

        # Order 2 for Sarah
        ("2024-01-25 20:00", 1,'Bella Italia',4, "Sarah", "Miller", '101 Elm St', 'Minestrone Soup x1\nTiramisu x2\n', "Morbi mollis diam"),

        # Order 1 for David
        ("2024-01-24 18:15", 4, 'Sushi Heaven',5, 'David', 'Wilson', "202 Maple St", 'Sashimi Platter x4\nSake x1\n', "bibendum nisi vitae"),

        # Order 2 for David
        ("2024-01-25 20:00", 4, 'Sushi Heaven',5, 'David', 'Wilson', '202 Maple St', 'Spicy Tuna Roll x8\nMiso Soup x999\n', "Phasellus commodo"),
    ]

    
    i=1
    for customer in customers:
        DBfuncs.registerCustomer(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5])
    for restaurant in restaurants:
        DBfuncs.registerRestaurant(restaurant[0], restaurant[1], restaurant[2], restaurant[3])
        DBfuncs.setTime(i, restaurant[4], restaurant[5])
        i += 1
    for item in menu_items:
        temp = list(item)
        temp.append(item[3] + '.png')
        item = tuple(temp)
        DBfuncs.addNewItem(item[0], item[1], item[2], item[3], item[4], item[5])
    for postcode in restaurant_postcodes:
        DBfuncs.addNewPostcode(postcode[0], postcode[1])
    for order in orders:
        DBfuncs.addNewOrder(order[0], order[1], order[2], order[3], order[4], order[5], order[6], order[7], order[8])
        
if __name__ == "__main__":
    DBfuncs.createTables()
    initExampleDB()