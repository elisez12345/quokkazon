
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user
from .models.seller import Seller
from .models.user import User
from .models.product import Product
from .models.purchase import Purchase
import datetime

bp = Blueprint('allpurchases', __name__)

@bp.route('/allpurchases', methods=['GET', 'POST'])
def allpurchases(): 
    if request.method == 'POST':
        uid = request.form.get('uid')
        # Fetch all purchases for the given uid since a very old date
        if uid != '' and uid.isnumeric():
            purchases = Purchase.get_all_by_uid_since(uid, datetime.datetime(1980, 1, 1, 0, 0, 0))
            return render_template('allpurchases.html', purchases=purchases)
        else:
            return jsonify({}), 404
    return render_template('allpurchases.html', purchases=[])

@bp.route('/orders', methods=['GET', 'POST'])
def orders():
    # find the products current user has bought:
    if current_user.is_authenticated:
        orders = Purchase.get_all_by_sid(
            current_user.id)
    else:
        orders = None
    # render the page by adding information to the index.html file
    return render_template('orders.html',
                           orders=orders,
                           is_seller=Seller.is_seller(current_user),
                           product_class=Product,
                           user_class=User)

@bp.route('/orders/fulfill/<int:uid>-<int:sid>-<int:pid>-<int:oid>', methods=['POST'])
def fulfill(uid, sid, pid, oid):
    current_dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if Purchase.fulfill(uid, sid, pid, oid, current_dateTime):
        return redirect(url_for('allpurchases.orders'))
    else:
        print("ERROR")
    return redirect(url_for('allpurchases.orders'))
        