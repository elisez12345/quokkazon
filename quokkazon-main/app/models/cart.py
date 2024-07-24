from flask import current_app as app

class CartItem:
    def __init__(self, uid, sid, pid, quantity, price, saved_for_later):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.price = price
        self.saved_for_later = saved_for_later

    @staticmethod
    def get(uid, sid, pid):
        rows = app.db.execute('''
SELECT *
FROM Cart
WHERE uid = :uid AND sid = :sid AND pid = :pid
''',
                              uid=uid,
                              sid = sid,
                              pid = pid)
        return CartItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT uid, Cart.sid, Cart.pid, Cart.quantity, price, saved_for_later
FROM Cart, Inventory
WHERE uid = :uid AND Cart.sid = Inventory.sid AND Cart.pid = Inventory.pid
''', uid = uid)
        return [CartItem(*row) for row in rows]
    
    @staticmethod
    def get_total_price(uid):
        rows = app.db.execute("""
        WITH C(total) AS
            (SELECT Cart.quantity * price FROM Cart, Inventory
            WHERE uid = :uid AND Cart.sid = Inventory.sid AND Cart.pid = Inventory.pid)
        SELECT SUM(total)
        FROM C
        """,
        uid=uid)
        return float(rows[0][0]) if rows and rows[0][0] is not None else 0.0
    
    @staticmethod
    def add_item(uid, sid, pid, quantity, saved_for_later):
        rows = app.db.execute("""
        INSERT INTO CART(uid, sid, pid, quantity, saved_for_later)
        VALUES(:uid, :sid, :pid, :quantity, :saved_for_later)
        """,
        uid=uid,
        sid = sid,
        pid = pid,
        quantity = quantity,
        saved_for_later = '0')
        return
    
    @staticmethod
    def remove_item(uid, sid, pid):
        rows = app.db.execute("""
        DELETE FROM CART
        WHERE uid = :uid AND sid = :sid AND pid = :pid
        """,
        uid=uid,
        sid=sid,
        pid=pid)
        return
    
    @staticmethod
    def update_quantity(uid, sid, pid, quantity):
        rows = app.db.execute("""
        UPDATE CART
        SET quantity = :quantity
        WHERE uid = :uid AND sid = :sid AND pid = :pid
        """,
        uid=uid,
        sid=sid,
        pid=pid,
        quantity=quantity)
        return

    @staticmethod
    def submit(uid):
        rows = app.db.execute("""
        DELETE FROM CART
        WHERE uid = :uid
        """,
        uid=uid)
        return

    @staticmethod
    def newOrderId(uid):
        rows = app.db.execute("""
        WITH orders(ids) AS (SELECT order_id
        FROM PURCHASES
        WHERE uid = :uid)
        SELECT MAX(orders.ids)
        FROM orders
        """, uid = uid)
        return int(rows[0][0]+1) if rows and rows[0][0] is not None else 1
    @staticmethod
    def newPurchase(uid, sid, pid, order_id, quantity, date_fulfilled):
        rows = app.db.execute("""
        INSERT INTO PURCHASES(uid, sid, pid, order_id, quantity, date_fulfilled)
        VALUES(:uid, :sid, :pid, :order_id, :quantity, :date_fulfilled)
        """, uid = uid, sid = sid, pid = pid, order_id=order_id, quantity = quantity, date_fulfilled= date_fulfilled
        )
        return
    
    @staticmethod
    def get_all_sids(uid):
        rows = app.db.execute('''
        SELECT DISTINCT sid
        FROM Cart
        WHERE uid = :uid
        ''', uid = uid)
        return [row[0] for row in rows]

    @staticmethod
    def increase_balances(sids, uid):
        for sid in sids:
            rows = app.db.execute('''
            WITH C(total) AS
            (SELECT Cart.quantity * price FROM Cart, Inventory
            WHERE uid = :uid AND Cart.sid = :sid AND Cart.pid = Inventory.pid)
            UPDATE USERS
            SET balance = balance + (SELECT SUM(total) FROM C)
            WHERE id = :sid
            ''', sid = sid, uid = uid)
        return

    @staticmethod
    def decrease_balance(uid):
        rows = app.db.execute('''
        WITH C(total) AS
            (SELECT Cart.quantity * price FROM Cart, Inventory
            WHERE uid = :uid AND Cart.sid = Inventory.sid AND Cart.pid = Inventory.pid)
        UPDATE USERS
        SET balance = balance - (SELECT SUM(total) FROM C)
        WHERE id = :uid
        ''', uid = uid)
        return

    