from flask import render_template, request, flash
from flask_login import current_user
from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField
from wtforms.validators import NumberRange, DataRequired, EqualTo
import datetime

from .models.inventory import Inventory
from .models.seller import Seller
from .models.product import Product

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/inventory')
def inventory():
    # find the products current user has bought:
    if current_user.is_authenticated:
        inventory = Inventory.get_all_by_sid(
            current_user.id)
    else:
        inventory = None
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                           avail_inventory=inventory,
                           is_seller=Seller.is_seller(current_user),
                           product_class=Product)

class InventoryEdit(FlaskForm):
    quantity = IntegerField('Quantity', validators=[NumberRange(min=0)])
    num_for_sale = IntegerField('For sale (≤ Quantity)', validators=[NumberRange(min=0,)])
    price = FloatField('Price', validators=[NumberRange(min=0,)])
    save = SubmitField('Save')


@bp.route('/inventory/edit/<int:product_id>/<int:oq>-<int:on>:<float:op>', methods=['GET', 'POST'])
def edit(product_id, oq, on, op):
    form = InventoryEdit()
    if form.validate_on_submit():
        if Inventory.edit(product_id,
                          current_user.id,
                          form.quantity.data,
                          form.num_for_sale.data,
                          form.price.data
                         ):
            return redirect(url_for('inventory.inventory'))
    return render_template('editInventory.html', title="Edit Item", form=form, old_quantity=oq, old_num_for_sale=on, old_price=op, product_name=Product.get_name(product_id), product_id=product_id)

@bp.route('/inventory/add/<int:product_id>', methods=['GET','POST'])
def add(product_id):
    default_quantity = 0
    default_num_for_sale = 0
    default_price = 0
    if Inventory.add(product_id, current_user.id, default_quantity, default_num_for_sale, default_price):
        return redirect(url_for('inventory.edit', product_id=product_id, oq=default_quantity, on=default_num_for_sale, op=default_price))
    flash(Product.get_name(product_id) + ' already present in inventory!')
    return redirect(url_for('inventory.inventory'))

@bp.route('/inventory/delete/<int:product_id>', methods=['GET', 'POST'])
def delete(product_id):
    flash(Product.get_name(product_id) + ' deleted from inventory!')
    Inventory.delete(product_id, current_user.id)
    return redirect(url_for('inventory.inventory'))