from flask import current_app as app

class Stock:
    def __init__(self, pid, name, description, image, altTxt, createdAt, updatedAt, price):
        self.pid = pid
        self.name = name
        self.description = description
        self.image = image
        self.altTxt = altTxt
        self.CreatedAt = createdAt
        self.UpdatedAt = updatedAt
        self.price = price

    @staticmethod
    def get_all_in_stock():
        rows = app.db.execute('''
        SELECT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.createdAt, Products.updatedAt, Inventory.price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        ''')
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_stock_desc():
        rows = app.db.execute('''
        SELECT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.createdAt, Products.updatedAt, Inventory.price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        ORDER BY Inventory.price DESC
        ''')
        return [Stock(*row) for row in rows]
    
    @staticmethod
    def get_all_in_stock():
        rows = app.db.execute('''
        SELECT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.createdAt, Products.updatedAt, Inventory.price
        FROM Products
        JOIN Inventory ON Products.pid = Inventory.pid
        ORDER BY Inventory.price ASC
        ''')
        return [Stock(*row) for row in rows]
