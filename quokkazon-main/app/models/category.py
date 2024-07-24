from flask import current_app as app

class Category:
    # def __init__(self, pid, name):
    #     self.pid = pid
    #     self.name = name
    
    def __init__(self, pid, name, description, image, altTxt, createdAt, updatedAt, category):
        self.pid = pid
        self.name = name
        self.description = description
        self.image = image
        self.altTxt = altTxt
        self.CreatedAt = createdAt
        self.UpdatedAt = updatedAt
        self.category = category

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.createdAt, Products.updatedAt, Category.name
        FROM Products
        JOIN Category ON Products.pid = Category.pid
        ''')
        return [Category(*row) for row in rows]
    
    def get_all_by_pid(pid):
        rows = app.db.execute('''
        SELECT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.createdAt, Products.updatedAt, Category.name
        FROM Products
        JOIN Category ON Products.pid = Category.pid
        WHERE pid = :pid
        ''', pid=pid)
        return [Category(*row) for row in rows]
    
    def get_all_by_cat(category):
        rows = app.db.execute('''
        SELECT Products.pid, Products.name, Products.description, Products.image, Products.altTxt, Products.createdAt, Products.updatedAt, Category.name as category
        FROM Products
        JOIN Category ON Products.pid = Category.pid
        WHERE Category.name = :category
        ''', category=category)
        return [Category(*row) for row in rows]

    def get_all_categories():
        rows = app.db.execute('''
        SELECT DISTINCT Category.name
        FROM Products
        JOIN Category ON Products.pid = Category.pid
        ''')
        return rows