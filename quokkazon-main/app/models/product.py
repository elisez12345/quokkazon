from flask import current_app as app

class Product:
    def __init__(self, pid, name, description, image, altTxt, createdAt, updatedAt):
        self.pid = pid
        self.name = name
        self.description = description
        self.image = image
        self.altTxt = altTxt
        self.CreatedAt = createdAt
        self.UpdatedAt = updatedAt

    @staticmethod
    def get(pid):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE pid = :pid
        ''', pid=pid)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM Products
        ''')
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_name(pid):
        product = Product.get(pid)
        if product != None:
            return product.name
        else:
            return None
        
    def newPID():
        rows = app.db.execute("""
        SELECT MAX(pid)
        FROM Products
        """)
        return rows
        
    @staticmethod 
    def add_product(pid, name, description, image, altTxt, createdAt, updatedAt):
        app.db.execute("""
        INSERT INTO Products(pid, name, description, image, altTxt, createdAt, updatedAt)
        VALUES(:pid, :name, :description, :image, :altTxt, :createdAt, :updatedAt)
        """, 
        pid = pid, 
        name=name, 
        description=description, 
        image=image, altTxt=altTxt, 
        createdAt=createdAt, 
        updatedAt=updatedAt
        )
        return
