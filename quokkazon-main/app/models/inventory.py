from flask import current_app as app

class Inventory:
    def __init__(self, sid, pid, quantity, num_for_sale, price):
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.num_for_sale = num_for_sale
        self.price = price

    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
        SELECT *
        FROM Inventory
        WHERE sid = :sid
        ''', sid=sid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_all_by_pid(pid):
        rows = app.db.execute('''
        SELECT *
        FROM Inventory
        WHERE pid = :pid
        ''', pid=pid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM Inventory
        ''')
        return [Inventory(*row) for row in rows]

    @staticmethod
    def edit(pid, sid, quantity, num_for_sale, price):
        try:
            rows = app.db.execute("""
            UPDATE Inventory
            SET quantity=:quantity, num_for_sale=:num_for_sale, price=:price
            WHERE pid=:pid AND sid=:sid
            """,
                                  pid=pid,
                                  sid=sid, 
                                  quantity=quantity,
                                  num_for_sale=num_for_sale,
                                  price=price
                                )
            return pid, sid
        except Exception as e:
            print(str(e))
    
    @staticmethod
    def add(pid, sid, quantity, num_for_sale, price):
        try:
            rows = app.db.execute("""
            INSERT INTO Inventory(pid, sid, quantity, num_for_sale, price)
            VALUES(:pid, :sid, :quantity, :num_for_sale, :price)
            """,
                                  pid=pid,
                                  sid=sid,
                                  quantity=quantity,
                                  num_for_sale=num_for_sale,
                                  price=price
                                )
            return pid, sid
        except Exception as e:
            print(str(e))

    @staticmethod
    def delete(pid, sid):
        try:
            rows = app.db.execute("""
            DELETE FROM Inventory
            WHERE pid=:pid AND sid=:sid
            """,
                                  pid=pid,
                                  sid=sid
                                )
            return pid, sid
        except Exception as e:
            print(str(e))