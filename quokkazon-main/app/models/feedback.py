from flask import current_app as app

class ProductFeedback:
    def __init__(self,uid,name,pid,rating,review,date_time):
        self.uid = uid
        self.name = name
        self.pid = pid
        self.rating = rating
        self.review = review
        self.date_time = date_time

    def summary_ratings(pid): 
        info = app.db.execute('''
        SELECT COUNT(f.rating), AVG(f.rating)
        FROM ProductFeedback as f
        WHERE f.pid = :pid
        ''', pid=pid)
        if info[0][1] is None:
            return (None,0)
        num = info[0][0]
        avg = round(info[0][1],1)
        return (avg,num)

    def all_pids(): 
        info = app.db.execute('SELECT pid FROM ProductFeedback')
        return info
    
    # current user's ratings and reviews (sorted in reverse chronological order)
    @staticmethod
    def get_by_uid_sort_date_descending(uid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        ORDER BY f.date_time DESC, p.name
        ''',
        uid=uid)
        return [ProductFeedback(*row) for row in rows]
    
    # current user's ratings and reviews (sorted in chronological order)
    @staticmethod
    def get_by_uid_sort_date_ascending(uid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        ORDER BY f.date_time, p.name
        ''',
        uid=uid)
        return [ProductFeedback(*row) for row in rows]
    
    # current user's ratings and reviews (sorted by rating from high to low)
    @staticmethod
    def get_by_uid_sort_rating_descending(uid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        ORDER BY f.rating DESC, p.name
        ''',
        uid=uid)
        return [ProductFeedback(*row) for row in rows]
    
    # current user's ratings and reviews (sorted by rating from low to high)
    @staticmethod
    def get_by_uid_sort_rating_ascending(uid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        ORDER BY f.rating, p.name
        ''',
        uid=uid)
        return [ProductFeedback(*row) for row in rows]
    
    # get all feedback for a given product (sorted in reverse chronological order)
    @staticmethod
    def get_by_pid_sort_date_descending(pid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u
        WHERE f.pid = :pid
        AND f.uid = u.id
        ORDER BY f.date_time DESC, name ASC
        ''',
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    # get all feedback for a given product (sorted in chronological order)
    @staticmethod
    def get_by_pid_sort_date_ascending(pid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u
        WHERE f.pid = :pid
        AND f.uid = u.id
        ORDER BY f.date_time ASC, name ASC
        ''',
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    # get all feedback for a given product (sorted by rating from high to low) 
    @staticmethod
    def get_by_pid_sort_rating_descending(pid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u
        WHERE f.pid = :pid
        AND f.uid = u.id
        ORDER BY f.rating DESC, name ASC
        ''',
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    # get all feedback for a given product (sorted by rating from low to high) 
    @staticmethod
    def get_by_pid_sort_rating_ascending(pid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u
        WHERE f.pid = :pid
        AND f.uid = u.id
        ORDER BY f.rating ASC, name ASC
        ''',
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE p.pid = f.pid
        ORDER BY f.rating DESC
        ''')
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_pid(uid, pid):
        rows = app.db.execute('''
        SELECT f.uid, p.name, f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Products as p
        WHERE f.uid = :uid
        AND p.pid = f.pid
        AND f.pid = :pid
        ORDER BY f.date_time DESC
        ''',
        uid=uid,
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def edit_rating(uid,pid,rating,time_updated):
        app.db.execute("""
        UPDATE ProductFeedback 
        SET rating = :rating, date_time = :time_updated                       
        WHERE uid = :uid 
        AND pid = :pid 
        """,
        uid=uid,
        pid=pid,
        rating=rating,
        time_updated = time_updated)
    
    @staticmethod
    def edit_review(uid,pid,review,time_updated):
        app.db.execute("""
        UPDATE ProductFeedback 
        SET review = :review, date_time = :time_updated                       
        WHERE uid = :uid 
        AND pid = :pid 
        """,
        uid=uid,
        pid=pid,
        review=review,
        time_updated = time_updated)
    
    @staticmethod
    def remove_feedback(uid,pid):
        app.db.execute("""
        DELETE from ProductFeedback 
        WHERE uid = :uid 
        AND pid = :pid 
        """,
        uid=uid,
        pid=pid)
    
    @staticmethod
    def feedback_exists(uid,pid): 
        exists = app.db.execute("""
        SELECT f.uid
        FROM ProductFeedback f                         
        WHERE f.uid = :uid
        AND f.pid = :pid 
        """,
        uid=uid,
        pid=pid)
        return exists 
    
    @staticmethod
    def has_purchased(uid,pid): 
        purchased = app.db.execute("""
        SELECT p.uid
        FROM Purchases p                           
        WHERE p.uid = :uid
        AND p.pid = :pid 
        """,
        uid=uid,
        pid=pid)
        return purchased 

    @staticmethod 
    def add_feedback(uid,pid,rating,review,time): 
        app.db.execute("""
        INSERT INTO ProductFeedback VALUES (:uid,:pid,:rating,:review,:date_time)
        """,
        uid=uid,
        pid=pid,
        rating=rating,
        review=review,
        date_time=time)
    
    @staticmethod 
    def get_product_name(pid): 
        name = app.db.execute("""
        SELECT name 
        FROM Products
        WHERE pid = :pid
        """,
        pid=pid)
        return name 


class SellerFeedback:
    def __init__(self,uid,name,sid,rating,review,date_time):
        self.uid = uid
        self.sid = sid
        self.name = name
        self.rating = rating
        self.review = review
        self.date_time = date_time

    def summary_ratings(sid): 
        info = app.db.execute('''
        SELECT COUNT(f.rating), AVG(f.rating)
        FROM SellectFeedback as f
        WHERE f.sid = :sid
        ''', sid=sid)
        num = info[0][0]
        avg = round(info[0][1],1)
        return (avg,num)
    # current user's ratings and reviews (sorted in reverse chronological order)
    @staticmethod
    def get_by_uid_sort_date_descending(uid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        ORDER BY f.date_time DESC, name
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    # current user's ratings and reviews (sorted in chronological order)
    @staticmethod
    def get_by_uid_sort_date_ascending(uid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        ORDER BY f.date_time DESC, name
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    # current user's ratings and reviews (sorted by rating from high to low)
    @staticmethod
    def get_by_uid_sort_rating_descending(uid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        ORDER BY f.rating DESC, name
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    # current user's ratings and reviews (sorted by rating from low to high)
    @staticmethod
    def get_by_uid_sort_rating_ascending(uid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        ORDER BY f.rating DESC, name
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_sid(uid, sid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        AND f.sid = :sid
        ORDER BY f.date_time DESC,name
        ''',
        uid=uid,
        sid=sid)
        return [SellerFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_sort_rating(uid):
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE f.uid = :uid
        AND s.id = f.sid
        ORDER BY f.rating DESC,name
        ''',
        uid=uid)
        return [SellerFeedback(*row) for row in rows]
    
    # get all feedback for a given seller (sorted in reverse chronological order)
    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u
        WHERE f.pid = :pid
        AND f.uid = u.id
        ORDER BY f.date_time DESC, name
        ''',
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_by_pid_sort_rating(pid):
        rows = app.db.execute('''
        SELECT f.uid, (u.firstname || ' ' || u.lastname) as name , f.pid, f.rating, f.review, f.date_time
        FROM ProductFeedback as f, Users as u
        WHERE f.pid = :pid
        AND f.uid = u.id
        ORDER BY f.rating DESC, name
        ''',
        pid=pid)
        return [ProductFeedback(*row) for row in rows]
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT f.uid, (s.firstname || ' ' || s.lastname) AS name, f.sid, f.rating, f.review, f.date_time
        FROM SellerFeedback as f, Users as s
        WHERE s.id = f.sid
        ''')
        return [SellerFeedback(*row) for row in rows]

    @staticmethod
    def edit_rating(uid,sid,rating,time_updated):
        app.db.execute("""
        UPDATE SellerFeedback 
        SET rating = :rating, date_time = :time_updated                       
        WHERE uid = :uid 
        AND sid = :sid 
        """,
        uid=uid,
        sid=sid,
        rating=rating,
        time_updated = time_updated)
    
    @staticmethod
    def edit_review(uid,sid,review,time_updated):
        app.db.execute("""
        UPDATE SellerFeedback 
        SET review = :review, date_time = :time_updated                       
        WHERE uid = :uid 
        AND sid = :sid 
        """,
        uid=uid,
        sid=sid,
        review=review,
        time_updated = time_updated)

    @staticmethod
    def remove_feedback(uid,sid):
        app.db.execute("""
        DELETE from SellerFeedback 
        WHERE uid = :uid 
        AND sid = :sid 
        """,
        uid=uid,
        sid=sid)
    
    @staticmethod 
    def add_feedback(uid,sid,rating,review,time): 
        app.db.execute("""
        INSERT INTO SellerFeedback VALUES (:uid,:sid,:rating,:review,:date_time)
        """,
        uid=uid,
        sid=sid,
        rating=rating,
        review=review,
        date_time=time)

    @staticmethod 
    def get_seller_name(sid): 
        name = app.db.execute("""
        SELECT (firstname || ' ' || lastname) AS name 
        FROM Users
        WHERE id = :sid
        """,
        sid=sid)
        return name[0][0] 