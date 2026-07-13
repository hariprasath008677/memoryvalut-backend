# Seeding data for the Waffle Shop POS System

CATEGORIES = [
    "Waffles",
    "Waffwich",
    "Bisky Waffles",
    "Fruitfull Crunches",
    "Churros",
    "Hot Chocoholic",
    "Chocolisious",
    "Choco Bites",
    "Bombolinis",
    "Sandwich",
    "Long Bun Sandwich",
    "Fries",
    "Maggi",
    "Milkshakes",
    "Coffee Delights",
    "Fizzy Pops",
    "Add-ons"
]

CATEGORY_IMAGES = {
    "Waffles": "https://images.unsplash.com/photo-1562376502-6f769499c886?auto=format&fit=crop&w=300&h=300&q=80",
    "Waffwich": "https://images.unsplash.com/photo-1621303837474-0f2c41f71acb?auto=format&fit=crop&w=300&h=300&q=80",
    "Bisky Waffles": "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=300&h=300&q=80",
    "Fruitfull Crunches": "https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?auto=format&fit=crop&w=300&h=300&q=80",
    "Churros": "https://images.unsplash.com/photo-1596781254308-41005ca59f13?auto=format&fit=crop&w=300&h=300&q=80",
    "Hot Chocoholic": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=300&h=300&q=80",
    "Chocolisious": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=300&h=300&q=80",
    "Choco Bites": "https://images.unsplash.com/photo-1511381939415-e44015466834?auto=format&fit=crop&w=300&h=300&q=80",
    "Bombolinis": "https://images.unsplash.com/photo-1530631673369-bc24f5803c5f?auto=format&fit=crop&w=300&h=300&q=80",
    "Sandwich": "https://images.unsplash.com/photo-1539252554453-80ab65ce3586?auto=format&fit=crop&w=300&h=300&q=80",
    "Long Bun Sandwich": "https://images.unsplash.com/photo-1509722747041-616f39b57569?auto=format&fit=crop&w=300&h=300&q=80",
    "Fries": "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=300&h=300&q=80",
    "Maggi": "https://images.unsplash.com/photo-1612927601601-6638404737ce?auto=format&fit=crop&w=300&h=300&q=80",
    "Milkshakes": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=300&h=300&q=80",
    "Coffee Delights": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=300&h=300&q=80",
    "Fizzy Pops": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=300&h=300&q=80",
    "Add-ons": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=300&h=300&q=80"
}

PRODUCTS = [
    # Waffles
    {"name": "Maple & Butter", "price": 99.00, "category": "Waffles"},
    {"name": "Belgian Choco", "price": 119.00, "category": "Waffles"},
    {"name": "Nutty Nutella", "price": 139.00, "category": "Waffles"},
    {"name": "Crunchy KitKat", "price": 119.00, "category": "Waffles"},
    {"name": "Dark & White Choco", "price": 119.00, "category": "Waffles"},
    {"name": "3 Chocolate", "price": 119.00, "category": "Waffles"},
    {"name": "Overloaded Chocolate", "price": 119.00, "category": "Waffles"},
    {"name": "Crunchy Ferrero", "price": 139.00, "category": "Waffles"},
    {"name": "Kookies & Kream", "price": 139.00, "category": "Waffles"},
    {"name": "Crunchy Biscof", "price": 139.00, "category": "Waffles"},
    {"name": "Pinky Velvet", "price": 139.00, "category": "Waffles"},
    
    # Waffwich
    {"name": "Maple & Butter Waffwich", "price": 99.00, "category": "Waffwich"},
    {"name": "Belgian Choco Waffwich", "price": 119.00, "category": "Waffwich"},
    {"name": "Nutty Nutella Waffwich", "price": 139.00, "category": "Waffwich"},
    {"name": "Crunchy KitKat Waffwich", "price": 119.00, "category": "Waffwich"},
    {"name": "Dark & White Choco Waffwich", "price": 119.00, "category": "Waffwich"},
    {"name": "3 Chocolate Waffwich", "price": 119.00, "category": "Waffwich"},
    {"name": "Overloaded Chocolate Waffwich", "price": 119.00, "category": "Waffwich"},
    {"name": "Crunchy Ferrero Waffwich", "price": 139.00, "category": "Waffwich"},
    {"name": "Kookies & Kream Waffwich", "price": 139.00, "category": "Waffwich"},
    {"name": "Crunchy Biscof Waffwich", "price": 139.00, "category": "Waffwich"},
    {"name": "Pinky Velvet Waffwich", "price": 139.00, "category": "Waffwich"},
    
    # Bisky Waffles
    {"name": "Maple & Butter Bisky Waffle", "price": 89.00, "category": "Bisky Waffles"},
    {"name": "Belgian Choco Bisky Waffle", "price": 99.00, "category": "Bisky Waffles"},
    {"name": "Nutty Nutella Bisky Waffle", "price": 129.00, "category": "Bisky Waffles"},
    {"name": "Crunchy KitKat Bisky Waffle", "price": 99.00, "category": "Bisky Waffles"},
    {"name": "Dark & White Choco Bisky Waffle", "price": 99.00, "category": "Bisky Waffles"},
    {"name": "3 Chocolate Bisky Waffle", "price": 99.00, "category": "Bisky Waffles"},
    {"name": "Overloaded Chocolate Bisky Waffle", "price": 99.00, "category": "Bisky Waffles"},
    {"name": "Crunchy Ferrero Bisky Waffle", "price": 129.00, "category": "Bisky Waffles"},
    {"name": "Kookies & Kream Bisky Waffle", "price": 119.00, "category": "Bisky Waffles"},
    {"name": "Crunchy Biscof Bisky Waffle", "price": 129.00, "category": "Bisky Waffles"},
    {"name": "Pinky Velvet Bisky Waffle", "price": 129.00, "category": "Bisky Waffles"},
    
    # Fruitfull Crunches
    {"name": "Fruit Exotica", "price": 169.00, "category": "Fruitfull Crunches"},
    {"name": "Banoffee", "price": 159.00, "category": "Fruitfull Crunches"},
    {"name": "Very Berry", "price": 199.00, "category": "Fruitfull Crunches"},
    
    # Churros
    {"name": "Classic Churros", "price": 139.00, "category": "Churros"},
    {"name": "Nutella Churros", "price": 169.00, "category": "Churros"},
    {"name": "Biscoff Churros", "price": 169.00, "category": "Churros"},
    {"name": "Churro Bites", "price": 159.00, "category": "Churros"},
    {"name": "Loaded Churros", "price": 179.00, "category": "Churros"},
    
    # Hot Chocoholic
    {"name": "Hot Chocolate", "price": 119.00, "category": "Hot Chocoholic"},
    {"name": "Hot Choco Milo", "price": 139.00, "category": "Hot Chocoholic"},
    
    # Chocolisious
    {"name": "Classic Brownie", "price": 109.00, "category": "Chocolisious"},
    {"name": "Brownie With Ice Cream", "price": 139.00, "category": "Chocolisious"},
    {"name": "Choco Lava", "price": 109.00, "category": "Chocolisious"},
    {"name": "Choco Lava With Ice Cream", "price": 139.00, "category": "Chocolisious"},
    
    # Choco Bites
    {"name": "Choco Brownie", "price": 139.00, "category": "Choco Bites"},
    {"name": "Choco Banana", "price": 139.00, "category": "Choco Bites"},
    {"name": "Choco Waffy", "price": 139.00, "category": "Choco Bites"},
    {"name": "Marshmallow Melts", "price": 139.00, "category": "Choco Bites"},
    
    # Bombolinis
    {"name": "Nutella Bombolini", "price": 119.00, "category": "Bombolinis"},
    {"name": "Pistachio Bombolini", "price": 119.00, "category": "Bombolinis"},
    {"name": "Caramel Bombolini", "price": 119.00, "category": "Bombolinis"},
    
    # Sandwich
    {"name": "Cheese Toast", "price": 89.00, "category": "Sandwich"},
    {"name": "Paneer Sandwich", "price": 119.00, "category": "Sandwich"},
    {"name": "Corn Cheese Sandwich", "price": 119.00, "category": "Sandwich"},
    {"name": "Veg Sandwich", "price": 109.00, "category": "Sandwich"},
    {"name": "Chilli Cheese Sandwich", "price": 109.00, "category": "Sandwich"},
    
    # Long Bun Sandwich
    {"name": "Veg Long Bun Sandwich", "price": 109.00, "category": "Long Bun Sandwich"},
    {"name": "Paneer Long Bun Sandwich", "price": 119.00, "category": "Long Bun Sandwich"},
    {"name": "Corn Cheese Long Bun Sandwich", "price": 119.00, "category": "Long Bun Sandwich"},
    
    # Fries
    {"name": "Classic Fries", "price": 119.00, "category": "Fries"},
    {"name": "Peri Peri Fries", "price": 129.00, "category": "Fries"},
    {"name": "Cheese Fries", "price": 129.00, "category": "Fries"},
    
    # Maggi
    {"name": "Classic Maggi", "price": 99.00, "category": "Maggi"},
    {"name": "Cheese Maggi", "price": 119.00, "category": "Maggi"},
    {"name": "Peri Peri Maggi", "price": 119.00, "category": "Maggi"},
    
    # Milkshakes
    {"name": "Chocolate", "price": 179.00, "category": "Milkshakes"},
    {"name": "Choco Oreo", "price": 179.00, "category": "Milkshakes"},
    {"name": "Nutella", "price": 179.00, "category": "Milkshakes"},
    {"name": "Ferrero Rocher", "price": 179.00, "category": "Milkshakes"},
    {"name": "Brownie", "price": 179.00, "category": "Milkshakes"},
    {"name": "Red Velvet", "price": 179.00, "category": "Milkshakes"},
    {"name": "KitKat", "price": 179.00, "category": "Milkshakes"},
    
    # Coffee Delights
    {"name": "Classic Cold Coffee", "price": 119.00, "category": "Coffee Delights"},
    {"name": "Caramel Cold Coffee", "price": 129.00, "category": "Coffee Delights"},
    {"name": "Choco Coffee", "price": 129.00, "category": "Coffee Delights"},
    
    # Fizzy Pops
    {"name": "Green Apple", "price": 139.00, "category": "Fizzy Pops"},
    {"name": "Litchi", "price": 139.00, "category": "Fizzy Pops"},
    {"name": "Strawberry", "price": 139.00, "category": "Fizzy Pops"},
    {"name": "Kiwi", "price": 139.00, "category": "Fizzy Pops"},
    {"name": "Blueberry", "price": 139.00, "category": "Fizzy Pops"},
    
    # Add-ons
    {"name": "Banana", "price": 0.00, "category": "Add-ons"},
    {"name": "Ice Cream Vanilla", "price": 30.00, "category": "Add-ons"},
    {"name": "Ice Cream Chocolate", "price": 30.00, "category": "Add-ons"},
    {"name": "Nutella Add-on", "price": 30.00, "category": "Add-ons"},
    {"name": "KitKat Bits", "price": 20.00, "category": "Add-ons"},
    {"name": "Choco Sprinkles", "price": 20.00, "category": "Add-ons"},
    {"name": "Cheese Slice", "price": 20.00, "category": "Add-ons"},
    {"name": "Mayo", "price": 20.00, "category": "Add-ons"}
]

PACKAGING_ITEMS = [
    {"name": "Cone", "current_stock": 250, "min_stock": 20},
    {"name": "Parcel Tray", "current_stock": 250, "min_stock": 20},
    {"name": "Pancake Tray", "current_stock": 250, "min_stock": 20},
    {"name": "350ml Cup", "current_stock": 250, "min_stock": 25},
    {"name": "250ml Cup", "current_stock": 250, "min_stock": 15}
]
