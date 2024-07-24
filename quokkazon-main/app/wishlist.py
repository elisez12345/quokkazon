from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime
from humanize import naturaltime

from .models.wishlist import WishListItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)


@bp.route('/wishlist')
def wishlist():
    # find the items the current user has added to their wishlist
    if current_user.is_authenticated:
        items = WishListItem.get_all_by_uid_since(
                        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)


@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    current_dateTime = datetime.datetime.now()
    WishListItem.add_item(current_user.id, product_id, current_dateTime)
    return redirect(url_for('wishlist.wishlist'))

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)
