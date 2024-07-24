from flask import current_app as app

class Seller:
    def __init__(self, sid):
        self.sid = sid

    @staticmethod
    def get(sid):
        rows = app.db.execute('''
        SELECT *
        FROM Seller
        WHERE sid = :sid
        ''',
        sid=sid)
        return Seller(*(rows[0])) if rows else None
        
    @staticmethod
    def is_seller(user):
        if hasattr(user,"id"):
            return Seller.get(user.id) != None
        return False

    @staticmethod
    def add_seller(id):
        try:
            app.db.execute("""
INSERT INTO Seller(sid)
VALUES(:id)
RETURNING sid
""",
                                  id=id)
            return None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None