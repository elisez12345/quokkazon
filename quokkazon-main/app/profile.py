
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from flask import Blueprint
bp = Blueprint('profile', __name__)

from .models.seller import Seller

@bp.route('/myprofile')
@login_required
def my_profile():
    a = Seller.get(current_user.id)

    if a is None: 
        is_seller = False
    else:
        is_seller = True

    # The user information will be loaded from the current_user proxy
    return render_template('myprofile.html',
                            is_seller = is_seller,
                           title='My Profile',
                           current_user=current_user)

@bp.route('/register_seller')
@login_required
def reg_seller():
    Seller.add_seller(current_user.id)
    # The user information will be loaded from the current_user proxy
    return redirect(url_for('profile.my_profile'))

