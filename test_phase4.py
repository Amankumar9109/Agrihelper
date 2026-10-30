import os
import sys
import json
from app import create_app
from extensions import db
from models.user import User
from models.order import Order, OrderItem
from models.cart import CartItem

def test_phase4():
    print("========================================")
    print("Starting Phase 4 Test Suite: Cart & Razorpay Store")
    print("========================================")
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        # 1. Test Product Catalog
        catalog_path = os.path.join(app.root_path, 'static', 'data', 'products.json')
        assert os.path.exists(catalog_path), f"products.json not found at {catalog_path}"
        with open(catalog_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        assert len(products) >= 12, f"Expected at least 12 products, got {len(products)}"
        first = products[0]
        assert 'id' in first and 'name' in first and 'price' in first and 'category' in first
        print(f"[OK] Product catalog loaded: {len(products)} products found")

        # Create a test user for authenticated flows
        test_email = "store_tester@agrihelper.local"
        user = User.query.filter_by(email=test_email).first()
        if not user:
            user = User(
                name="Store Tester",
                email=test_email,
                provider="local"
            )
            db.session.add(user)
        user.set_password("TestPassword123!")
        db.session.commit()
        user_id = user.id
        print(f"[OK] Test user ready (ID: {user_id})")

    client = app.test_client()

    # 2. Test Store Page
    res = client.get('/store')
    assert res.status_code == 200, f"Expected 200 from /store, got {res.status_code}"
    assert b"AgriHelper Farmer Store" in res.data or b"Store" in res.data
    print("[OK] GET /store rendered successfully")

    # 3. Test Cart Count API (initial)
    res = client.get('/api/cart/count')
    assert res.status_code == 200
    data = res.get_json()
    assert 'count' in data
    print(f"[OK] GET /api/cart/count returned count={data['count']}")

    # 4. Test Unauthenticated Cart Add (should return 401 auth_required)
    res = client.post('/store/cart/add', json={'product_id': 'seed-001', 'quantity': 1})
    assert res.status_code == 401
    unauth_data = res.get_json()
    assert unauth_data.get('auth_required') is True
    print("[OK] Unauthenticated cart add correctly returned 401 auth_required")

    # 5. Log in test user
    login_res = client.post('/login', data={'email': test_email, 'password': 'TestPassword123!'}, follow_redirects=True)
    assert login_res.status_code == 200
    print("[OK] Test user logged in")

    # 6. Test Authenticated Add to Cart
    res = client.post('/store/cart/add', json={'product_id': 'seed-001', 'quantity': 2})
    assert res.status_code == 200
    data = res.get_json()
    assert data.get('success') is True
    assert data.get('cart_count') >= 2
    print(f"[OK] Authenticated add to cart: added 2x product seed-001, cart count = {data.get('cart_count')}")

    # Add second product (seed-002)
    res = client.post('/store/cart/add', json={'product_id': 'seed-002', 'quantity': 1})
    assert res.status_code == 200
    print("[OK] Authenticated add to cart: added 1x product seed-002")

    # 7. Test Cart View
    res = client.get('/store/cart')
    assert res.status_code == 200
    assert b"Your Cart" in res.data or b"Shopping Cart" in res.data
    print("[OK] GET /store/cart rendered for authenticated user")

    # Fetch cart items from DB to get real item IDs
    with app.app_context():
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        assert len(cart_items) == 2
        item1 = next(i for i in cart_items if i.product_id == 'seed-001')
        item2 = next(i for i in cart_items if i.product_id == 'seed-002')
        item1_id = item1.id
        item2_id = item2.id

    # 8. Test Update Cart Quantity
    res = client.post('/store/cart/update', json={'item_id': item1_id, 'quantity': 3})
    assert res.status_code == 200
    data = res.get_json()
    assert data.get('success') is True
    assert data.get('item_quantity') == 3
    print(f"[OK] POST /store/cart/update updated item #{item1_id} quantity to 3")

    # 9. Test Remove from Cart
    res = client.post(f'/store/cart/remove/{item2_id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data.get('success') is True
    print(f"[OK] POST /store/cart/remove/{item2_id} removed item #2 from cart")

    # 10. Test Checkout Preparation (Create Razorpay Order)
    checkout_payload = {
        'shipping_name': 'Store Tester',
        'shipping_phone': '9876543210',
        'shipping_address': 'Farmhouse 42, Green Valley',
        'city': 'Nashik',
        'state': 'Maharashtra',
        'pincode': '422001',
        'payment_method': 'razorpay'
    }
    res = client.post('/store/checkout', json=checkout_payload)
    assert res.status_code == 200, f"Checkout failed: {res.data}"
    order_data = res.get_json()
    assert order_data.get('success') is True
    razorpay_order_id = order_data.get('razorpay_order_id')
    db_order_id = order_data.get('order_id')
    amount_inr = order_data.get('amount_display')
    assert razorpay_order_id is not None
    assert db_order_id is not None
    assert amount_inr > 0
    print(f"[OK] POST /store/checkout created Razorpay Order {razorpay_order_id} (DB Order #{db_order_id}, Rs. {amount_inr})")

    # 11. Test Payment Verification (Dev Test Simulation Mode)
    verify_payload = {
        'order_id': db_order_id,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': f'pay_sim_{db_order_id}_123456',
        'razorpay_signature': 'simulated_signature'
    }
    res = client.post('/store/verify_payment', json=verify_payload)
    assert res.status_code == 200, f"Verify payment failed: {res.data}"
    verify_data = res.get_json()
    assert verify_data.get('success') is True
    assert 'redirect_url' in verify_data
    print(f"[OK] POST /store/verify_payment successfully verified payment and captured order #{db_order_id}")

    # Verify Order is marked paid in DB and has order items
    with app.app_context():
        order = db.session.get(Order, db_order_id)
        assert order is not None
        assert order.status == 'paid'
        assert order.razorpay_payment_id == f'pay_sim_{db_order_id}_123456'
        items_count = order.items.count()
        assert items_count > 0
        print(f"[OK] Verified DB Order #{order.id}: status={order.status}, amount=Rs.{order.amount}, items_count={items_count}")

    # 12. Test Cart is Cleared after Successful Payment
    res = client.get('/api/cart/count')
    assert res.status_code == 200
    data = res.get_json()
    assert data.get('count') == 0, f"Expected empty cart after payment, got {data.get('count')}"
    print("[OK] Cart verified empty after checkout completion")

    # 13. Test Order Success Receipt Page
    res = client.get(f'/store/order/success/{db_order_id}')
    assert res.status_code == 200
    assert b"Order Confirmed" in res.data or b"Order #" in res.data
    assert str(db_order_id).encode() in res.data
    print(f"[OK] GET /store/order/success/{db_order_id} rendered tax invoice receipt successfully")

    # 14. Test Order History View
    res = client.get('/store/orders')
    assert res.status_code == 200
    assert b"My Orders" in res.data
    assert str(db_order_id).encode() in res.data
    print(f"[OK] GET /store/orders successfully listed order #{db_order_id} for authenticated user")

    print("========================================")
    print("ALL PHASE 4 TESTS PASSED (13/13)!")
    print("========================================")

if __name__ == '__main__':
    test_phase4()
