from flask import render_template
from flask import redirect, request, url_for, session
from flask_session import Session
from flask_login import current_user
from humanize import naturaltime
import datetime
from collections import defaultdict
import os, random

from .models.product import Product
from .models.feedback import ProductFeedback
from .models.inventory import Inventory
from .models.stock import Stock
from .models.category import Category
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('categories', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

ROWS = 24
@bp.route('/<category_name>', methods=['GET','POST'])
def category_products(category_name):
    page = request.args.get("page", 1, type=int)
    start = (page-1) * ROWS
    end = start + ROWS
    
    cat_items = Category.get_all_by_cat(category_name[2:-3])
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)
    items = Stock.get_all_in_stock()
    
    sort_by_price = request.args.get('sort', type=int)
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        summary[item.pid] = ProductFeedback.summary_ratings(item.pid)
    if sort_by_price:
        items = Stock.get_stock_desc()
    
    paginated = cat_items[start:end]
    total_pages = len(items)//24 + 1
    
    categories = Category.get_all_categories()
    
    return render_template('products2.html',
                      items=paginated,
                      inventory=inventory, 
                      summary=summary,
                      product_prices = product_prices,
                      page=page,
                      total_pages=total_pages,
                      categories=categories)
    
def sort_by_min_value(prices):
    return min(prices[1])
    

@bp.route('/products/search_results', methods=['GET','POST'])
def search_results():
    page = request.args.get("page", 1, type=int)
    start = (page-1) * ROWS
    end = start + ROWS
    
    search_term = request.args.get('search_term', '')
    # items = Product.get_all()
    inventory = Inventory.get_all()
    product_prices = defaultdict(list)
    summary = defaultdict(list)

    image_folder = '/home/ubuntu/quokkazon/app/static/product_images'
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    random_image = random.choice(image_files)
    
    for item in inventory:
        product_prices[item.pid].append(item.price)
        summary[item.pid] = ProductFeedback.summary_ratings(item.pid)
    if request.method == 'POST':
        search_term = request.form['search_term']
        session['search_term'] = search_term
        if not search_term:
            return redirect(url_for('products.products'))
    if request.method == 'GET':
        search_term = session.get('search_term')
    products = search_products(search_term)

    paginated = products[start:end]
    total_pages = len(products)//24 + 1
    return render_template('searchResults2.html',
                            items = products,
                            inventory = inventory,
                            image="product_images/"+random_image,
                            product_prices = product_prices,
                            search_term = search_term,
                            summary=summary,
                            len_products = len(products),
                            page=page,
                            total_pages=total_pages)
    
def search_products(search_term):
    products = Product.get_all()
    search_results = [product for product in products if (search_term.lower() in product.name.lower()) or (search_term.lower() in product.description.lower())]
    return search_results
    