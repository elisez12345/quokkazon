from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import redirect, url_for, request
import datetime
from humanize import naturaltime

from .models.cart import CartItem
from .models.inventory import Inventory
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    # find the items the current user has added to their wishlist
    if current_user.is_authenticated:
        items = CartItem.get_all_by_uid(
                        current_user.id)
        totalprice = CartItem.get_total_price(current_user.id)
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                      items=items, totalprice=totalprice)


@bp.route('/cart/add', methods=['POST'])
def cart_add():
    product_id = request.form["product_id"]
    seller_id = request.form["seller_id"]
    quantity = request.form["quantity"]
    saved_for_later = request.form["saved_for_later"]
    
    CartItem.add_item(current_user.id, seller_id, product_id, quantity, saved_for_later)
    print("I'M BUYING THIS MANY", quantity)
    return redirect(url_for('cart.cart'))

@bp.route('/cart/select/<int:product_id>', methods=['POST'])
def cart_select(product_id):
    # find the sellers for this product
    if current_user.is_authenticated:
        sellers = Inventory.get_all_by_pid(product_id)
    else:
        return jsonify({}), 404
    # render a seller selection page with seller IDs and prices
    return render_template('sellerselection.html',
                      sellers=sellers)

@bp.route('/cart/remove/<int:product_id>/<int:seller_id>', methods=['POST'])
def cart_remove(seller_id, product_id):
    CartItem.remove_item(current_user.id, seller_id, product_id)
    return redirect(url_for('cart.cart'))

@bp.route('/cart/update_quantity', methods=['POST'])
def cart_update_quantity():
    quantity = request.form['quantity']
    seller_id = request.form['seller_id']
    product_id = request.form['product_id']
    CartItem.update_quantity(current_user.id, seller_id, product_id, quantity)
    return redirect(url_for('cart.cart'))

@bp.route('/cart/submit', methods=['POST'])
def cart_submit():
    neworder = CartItem.newOrderId(current_user.id)
    CartItem.increase_balances(CartItem.get_all_sids(current_user.id), current_user.id)
    CartItem.decrease_balance(current_user.id)
    items = CartItem.get_all_by_uid(
                        current_user.id)
    for item in items:
        CartItem.newPurchase(item.uid, item.sid, item.pid, neworder, item.quantity, None)
    CartItem.submit(current_user.id)
    return redirect(url_for('cart.cart_order', order_id = neworder))

@bp.route('/cart/<int:order_id>')
def cart_order(order_id):
    items = Purchase.get_order(current_user.id, order_id)
    totalprice = Purchase.get_total_price_order(current_user.id, order_id)
    return render_template('buyerOrder.html', items = items, totalprice = totalprice)
