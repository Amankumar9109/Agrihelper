from flask import render_template, request, jsonify
from flask_login import current_user
from extensions import db
from models.cart import CartItem
from . import store_bp

@store_bp.route('/store')
def store():
    return render_template('store.html')

@store_bp.route('/api/cart/count')
def cart_count():
    if not current_user.is_authenticated:
        return jsonify({'count': 0})
    count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'count': count})
