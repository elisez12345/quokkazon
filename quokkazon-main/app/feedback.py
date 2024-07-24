from flask import jsonify
from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import datetime
from humanize import naturaltime

from .models.feedback import ProductFeedback, SellerFeedback

from flask import Blueprint
bp = Blueprint('feedback', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/myfeedback/<int:option>')
def my_feedback(option):
    if option == 1:
        # sort in chronological order  
        pfeedback = ProductFeedback.get_by_uid_sort_date_ascending(current_user.id)
        sfeedback = SellerFeedback.get_by_uid_sort_date_ascending(current_user.id)
    elif option == 2: 
        # sort by rating from high to low 
        pfeedback = ProductFeedback.get_by_uid_sort_rating_descending(current_user.id)
        sfeedback = SellerFeedback.get_by_uid_sort_rating_descending(current_user.id)
    elif option == 3:
        # sort by rating from low to high 
        pfeedback = ProductFeedback.get_by_uid_sort_rating_ascending(current_user.id)
        sfeedback = SellerFeedback.get_by_uid_sort_rating_ascending(current_user.id)
    else: 
        # default: sort in reverse chronological order
        pfeedback = ProductFeedback.get_by_uid_sort_date_descending(current_user.id)
        sfeedback = SellerFeedback.get_by_uid_sort_date_descending(current_user.id)

    return render_template('myfeedback.html',
                        pfeedback=pfeedback,
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/add/<int:product_id>/<name>', methods=['POST','GET'])
def product_submission_form(product_id,name):
    return render_template('myfeedback_add.html',
                            product_id=product_id,
                            name=name,
                            type="product",
                            humanize_time=humanize_time)

@bp.route('/myfeedback/add/product', methods=['POST','GET'])
def product_add_feedback():
    if request.method == 'POST': 
        pid = int(request.form['pid'])
        rating = int(request.form['rating'])
        review = request.form['review']
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductFeedback.add_feedback(current_user.id,pid,rating,review,current_dateTime)
        pfeedback = ProductFeedback.get_by_uid_pid(current_user.id, pid)
    return render_template('myfeedback_edit.html',
                        pfeedback=pfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/edit/product/<int:product_id>', methods=['POST','GET'])
def product_feedback_edit(product_id):
    pfeedback = ProductFeedback.get_by_uid_pid(current_user.id, product_id)
    return render_template('myfeedback_edit.html',
                        pfeedback=pfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/edit/product_rating', methods=['POST','GET'])
def product_rating_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rating = int(request.form['rating'])
        pid = int(request.form['pid'])
        ProductFeedback.edit_rating(current_user.id, pid, rating, current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))

@bp.route('/myfeedback/edit/product_review', methods=['POST','GET'])
def product_review_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        review = request.form['review']
        pid = int(request.form['pid'])
        ProductFeedback.edit_review(current_user.id, pid, review, current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))

@bp.route('/myfeedback/delete/<int:product_id>', methods=['POST','GET'])
def product_remove_feedback(product_id):
    if request.method == 'POST': 
        ProductFeedback.remove_feedback(current_user.id,product_id)
    return redirect(url_for('feedback.my_feedback',option=0))

@bp.route('/myfeedback/delete/product_review', methods=['POST','GET'])
def product_remove_review():
    if request.method == 'POST': 
        pid = int(request.form['pid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ProductFeedback.edit_review(current_user.id, pid,'',current_dateTime)
    return redirect(url_for('feedback.product_feedback_edit',product_id=pid))



@bp.route('/myfeedback/edit/seller/<int:seller_id>', methods=['POST','GET'])
def seller_feedback_edit(seller_id):
    sfeedback = SellerFeedback.get_by_uid_sid( # sorted by rating 
                    current_user.id, seller_id)
    return render_template('myfeedback_edit.html',
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/edit/seller_rating', methods=['POST','GET'])
def seller_rating_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rating = int(request.form['rating'])
        sid = int(request.form['sid'])
        SellerFeedback.edit_rating(current_user.id, sid, rating, current_dateTime)
    return redirect(url_for('feedback.seller_feedback_edit',seller_id=sid))

@bp.route('/myfeedback/edit/seller_review', methods=['POST','GET'])
def seller_review_edit():
    if request.method == 'POST': 
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        review = request.form['review']
        sid = int(request.form['sid'])
        SellerFeedback.edit_review(current_user.id, sid, review, current_dateTime)
    return redirect(url_for('feedback.seller_feedback_edit',seller_id=sid))

@bp.route('/myfeedback/delete', methods=['POST','GET'])
def seller_remove_feedback():
    if request.method == 'POST':
        sid = int(request.form['sid'])
        SellerFeedback.remove_feedback(current_user.id,sid)
    return redirect(url_for('feedback.my_feedback',option=0))

@bp.route('/myfeedback/delete/seller_review', methods=['POST','GET'])
def seller_remove_review():
    if request.method == 'POST': 
        seller_id = int(request.form['sid'])
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        SellerFeedback.edit_review(current_user.id, seller_id,'',current_dateTime)
    return redirect(url_for('feedback.seller_feedback_edit',seller_id=seller_id))

@bp.route('/myfeedback/add/seller', methods=['POST','GET'])
def seller_add_feedback():
    if request.method == 'POST': 
        sid = int(request.form['sid'])
        rating = int(request.form['rating'])
        review = request.form['review']
        current_dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        SellerFeedback.add_feedback(current_user.id,sid,rating,review,current_dateTime)
        sfeedback = SellerFeedback.get_by_uid_sid(current_user.id, sid)
    return render_template('myfeedback_edit.html',
                        sfeedback=sfeedback,
                        humanize_time=humanize_time)

@bp.route('/myfeedback/add/<int:seller_id>', methods=['POST','GET'])
def seller_submission_form(seller_id):
    name = SellerFeedback.get_seller_name(seller_id)
    print(name)
    return render_template('myfeedback_add.html',
                            seller_id=seller_id,
                            name=name,
                            type="seller",
                            humanize_time=humanize_time)