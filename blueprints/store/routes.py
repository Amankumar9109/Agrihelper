import os
import json
import secrets
from datetime import datetime, timedelta
import razorpay
from flask import render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from extensions import db
from models.cart import CartItem
from models.order import Order, OrderItem
from . import store_bp

def get_products():
    """Loads product catalog from products.json"""
    path = os.path.join(current_app.root_path, 'static', 'data', 'products.json')
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            current_app.logger.error(f"Error loading products.json: {e}")
    return []

def get_razorpay_client():
    """Initializes and returns razorpay client if keys are present"""
    key_id = current_app.config.get('RAZORPAY_KEY_ID') or os.getenv('RAZORPAY_KEY_ID')
    key_secret = current_app.config.get('RAZORPAY_KEY_SECRET') or os.getenv('RAZORPAY_KEY_SECRET')
    if key_id and key_secret:
        return razorpay.Client(auth=(key_id, key_secret)), key_id, key_secret
    return None, key_id or 'rzp_test_agrihelper_dev', key_secret or 'dev_secret_key'

@store_bp.route('/store')
def store():
    products = get_products()
    categories = sorted(list(set(p.get('category', 'General') for p in products)))
    selected_cat = request.args.get('category', 'All')

    if selected_cat and selected_cat != 'All':
        display_products = [p for p in products if p.get('category') == selected_cat]
    else:
        display_products = products

    return render_template(
        'store.html',
        products=display_products,
        categories=categories,
        selected_category=selected_cat
    )

@store_bp.route('/store/cart')
@store_bp.route('/cart')
@store_bp.route('/checkout')
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.price * item.quantity for item in items)
    shipping = 0.0 if (subtotal >= 999 or len(items) == 0) else 99.0
    total = round(subtotal + shipping, 2)

    return render_template(
        'cart.html',
        items=items,
        subtotal=round(subtotal, 2),
        shipping=round(shipping, 2),
        total=total
    )

@store_bp.route('/store/cart/add', methods=['POST'])
@store_bp.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'auth_required': True,
            'login_url': url_for('auth.login', next=url_for('store.store'))
        }), 401

    data = request.get_json() or {}
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    # Look up product in catalog
    products = get_products()
    matched = next((p for p in products if str(p['id']) == str(product_id)), None)
    if not matched:
        return jsonify({'error': 'Product not found'}), 404

    # Check if product is already in cart
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=str(product_id)).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(
            user_id=current_user.id,
            product_id=matched['id'],
            product_name=matched['name'],
            price=matched['price'],
            quantity=quantity,
            image_url=matched.get('image', '')
        )
        db.session.add(new_item)

    db.session.commit()

    total_count = sum(i.quantity for i in CartItem.query.filter_by(user_id=current_user.id).all())
    return jsonify({
        'success': True,
        'message': f"Added '{matched['name']}' to your cart!",
        'cart_count': total_count
    })

@store_bp.route('/store/cart/update', methods=['POST'])
@store_bp.route('/api/cart/update', methods=['POST'])
@login_required
def update_cart_item():
    data = request.get_json() or {}
    item_id = data.get('item_id')
    delta = int(data.get('delta', 0))
    new_qty = data.get('quantity')

    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Cart item not found'}), 404

    if new_qty is not None:
        item.quantity = max(0, int(new_qty))
    else:
        item.quantity = max(0, item.quantity + delta)

    if item.quantity <= 0:
        db.session.delete(item)
        db.session.commit()
        item_total = 0
    else:
        db.session.commit()
        item_total = round(item.price * item.quantity, 2)

    # Recalculate totals
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(i.price * i.quantity for i in items)
    shipping = 0.0 if (subtotal >= 999 or len(items) == 0) else 99.0
    total = round(subtotal + shipping, 2)
    cart_count = sum(i.quantity for i in items)

    return jsonify({
        'success': True,
        'item_id': item_id,
        'item_quantity': item.quantity if item_total > 0 else 0,
        'item_total': item_total,
        'subtotal': round(subtotal, 2),
        'shipping': round(shipping, 2),
        'total': total,
        'cart_count': cart_count
    })

@store_bp.route('/store/cart/remove/<int:item_id>', methods=['POST', 'DELETE'])
@store_bp.route('/api/cart/remove/<int:item_id>', methods=['POST', 'DELETE'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if item:
        db.session.delete(item)
        db.session.commit()

    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(i.price * i.quantity for i in items)
    shipping = 0.0 if (subtotal >= 999 or len(items) == 0) else 99.0
    total = round(subtotal + shipping, 2)
    cart_count = sum(i.quantity for i in items)

    return jsonify({
        'success': True,
        'subtotal': round(subtotal, 2),
        'shipping': round(shipping, 2),
        'total': total,
        'cart_count': cart_count
    })

@store_bp.route('/api/cart/count')
def cart_count():
    if not current_user.is_authenticated:
        return jsonify({'count': 0})
    count = sum(item.quantity for item in CartItem.query.filter_by(user_id=current_user.id).all())
    return jsonify({'count': count})

# Razorpay Checkout & Webhook Endpoints
@store_bp.route('/store/checkout', methods=['POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        return jsonify({'error': 'Your cart is empty'}), 400

    subtotal = sum(i.price * i.quantity for i in items)
    shipping = 0.0 if subtotal >= 999 else 99.0
    grand_total = round(subtotal + shipping, 2)
    amount_in_paise = int(round(grand_total * 100))

    data = request.get_json() or {}
    shipping_address = data.get('shipping_address', 'Farmer Farm Residence')
    phone_number = data.get('phone_number', '9876543210')

    # Create Order in DB
    order = Order(
        user_id=current_user.id,
        amount=grand_total,
        status='pending',
        shipping_address=shipping_address,
        phone_number=phone_number
    )
    db.session.add(order)
    db.session.flush()

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            product_name=item.product_name,
            price=item.price,
            quantity=item.quantity
        )
        db.session.add(order_item)

    # Razorpay Order Creation
    rzp_client, key_id, key_secret = get_razorpay_client()

    if rzp_client:
        try:
            rzp_order = rzp_client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'receipt': f'order_agri_{order.id}',
                'payment_capture': 1
            })
            order.razorpay_order_id = rzp_order['id']
        except Exception as e:
            current_app.logger.error(f"Razorpay API error: {e}")
            # Fallback for dev/testing
            order.razorpay_order_id = f"order_test_{order.id}_{secrets.token_hex(4)}"
    else:
        # Dev test mode fallback
        order.razorpay_order_id = f"order_dev_test_{order.id}_{secrets.token_hex(4)}"

    db.session.commit()

    return jsonify({
        'success': True,
        'razorpay_order_id': order.razorpay_order_id,
        'amount': amount_in_paise,
        'amount_display': grand_total,
        'currency': 'INR',
        'key_id': key_id,
        'order_id': order.id,
        'user_name': current_user.name,
        'user_email': current_user.email,
        'user_phone': phone_number,
        'is_test_mode': rzp_client is None
    })

@store_bp.route('/store/verify_payment', methods=['POST'])
@login_required
def verify_payment():
    data = request.get_json() or {}
    local_order_id = data.get('order_id')
    rzp_order_id = data.get('razorpay_order_id')
    rzp_payment_id = data.get('razorpay_payment_id')
    rzp_signature = data.get('razorpay_signature')
    address = data.get('address')
    phone = data.get('phone')

    if local_order_id:
        order = Order.query.filter_by(id=local_order_id, user_id=current_user.id).first()
    elif rzp_order_id:
        order = Order.query.filter_by(razorpay_order_id=rzp_order_id, user_id=current_user.id).first()
    else:
        order = None

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    rzp_client, key_id, key_secret = get_razorpay_client()

    # Signature verification
    signature_valid = False
    if rzp_client and rzp_signature and not rzp_order_id.startswith('order_dev_test'):
        try:
            rzp_client.utility.verify_payment_signature({
                'razorpay_order_id': rzp_order_id,
                'razorpay_payment_id': rzp_payment_id,
                'razorpay_signature': rzp_signature
            })
            signature_valid = True
        except Exception as e:
            current_app.logger.error(f"Razorpay signature verification failed: {e}")
            signature_valid = False
    else:
        # Test mode auto-verify
        signature_valid = True

    if not signature_valid:
        order.status = 'failed'
        db.session.commit()
        return jsonify({'error': 'Payment verification failed'}), 400

    # Mark order as paid
    order.status = 'paid'
    order.razorpay_payment_id = rzp_payment_id or f"pay_test_{secrets.token_hex(6)}"
    order.razorpay_signature = rzp_signature or 'dev_simulated_sig'
    if address:
        order.shipping_address = address
    if phone:
        order.phone_number = phone

    # Clear user cart items
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({
        'success': True,
        'order_id': order.id,
        'redirect_url': url_for('store.order_success', order_id=order.id)
    })

@store_bp.route('/store/order/success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    est_delivery = (order.created_at + timedelta(days=3)).strftime('%A, %d %B %Y')
    return render_template('order_success.html', order=order, estimated_delivery=est_delivery)

@store_bp.route('/store/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)
