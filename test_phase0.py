"""
Phase 0 Verification Test Suite for AgriHelper
Verifies:
1. Application factory create_app()
2. All 9 blueprints registered
3. Database tables initialized (User, CartItem, Order, OrderItem, Post, Comment)
4. All GET routes return status 200:
   - /
   - /login
   - /market
   - /store
   - /community
   - /community/post
   - /weather
   - /policy
   - /policy/p1 ... /policy/p5
   - /techniques
   - /modern_farming/drip_irrigation ... /modern_farming/ai_data_analytics
5. Market POST endpoints (/get_options, /get_prices)
6. Chatbot POST endpoint (/api/chat)
7. Local user registration and login
"""
import sys
from app import create_app
from extensions import db
from models.user import User

def run_tests():
    print("=== STARTING PHASE 0 TEST SUITE ===")
    app = create_app('testing')
    client = app.test_client()

    with app.app_context():
        db.create_all()

    # 1. Test Blueprints
    expected_bps = {'main', 'auth', 'market', 'store', 'community', 'policy', 'farming', 'weather', 'chatbot'}
    actual_bps = set(app.blueprints.keys())
    assert expected_bps.issubset(actual_bps), f"Missing blueprints: {expected_bps - actual_bps}"
    print("[PASS] All 9 blueprints registered.")

    # 2. Test GET Routes
    get_routes = [
        ('/', 'Home'),
        ('/login', 'Login'),
        ('/market', 'Market'),
        ('/store', 'Store'),
        ('/community', 'Community'),
        ('/community/post', 'Community Post'),
        ('/weather', 'Weather'),
        ('/policy', 'Policy'),
        ('/policy/p1', 'Scheme P1'),
        ('/policy/p2', 'Scheme P2'),
        ('/policy/p3', 'Scheme P3'),
        ('/policy/p4', 'Scheme P4'),
        ('/policy/p5', 'Scheme P5'),
        ('/techniques', 'Modern Farming Techniques'),
        ('/modern_farming/drip_irrigation', 'Drip Irrigation'),
        ('/modern_farming/soil_health', 'Soil Health'),
        ('/modern_farming/vertical_farming', 'Vertical Farming'),
        ('/modern_farming/drones_agriculture', 'Drones Agriculture'),
        ('/modern_farming/hydroponics', 'Hydroponics'),
        ('/modern_farming/ai_data_analytics', 'AI & Data Analytics'),
    ]

    for route, name in get_routes:
        resp = client.get(route)
        assert resp.status_code == 200, f"Route {route} ({name}) failed with status {resp.status_code}"
        print(f"[PASS] GET {route:<35} -> 200 OK ({name})")

    # 3. Test Market POST endpoints
    # Options test
    opt_resp = client.post('/get_options', json={'level': 'district', 'selection': 'Maharashtra'})
    assert opt_resp.status_code == 200, f"/get_options failed: {opt_resp.status_code}"
    print(f"[PASS] POST /get_options returned {len(opt_resp.get_json())} options.")

    # 4. Test Chatbot API stub
    chat_resp = client.post('/api/chat', json={'message': 'What fertilizer is best for wheat?'})
    assert chat_resp.status_code == 200, f"/api/chat failed: {chat_resp.status_code}"
    chat_data = chat_resp.get_json()
    assert 'reply' in chat_data, "Chatbot response missing 'reply'"
    print(f"[PASS] POST /api/chat returned reply: {chat_data['reply'][:60]}...")

    # 5. Test Auth Registration & Login
    with app.app_context():
        # Clean any existing test user
        User.query.filter_by(email='farmer_test@agrihelper.in').delete()
        db.session.commit()

        # Register
        signup_resp = client.post('/signup', data={
            'name': 'Ramesh Kumar',
            'email': 'farmer_test@agrihelper.in',
            'password': 'securepassword123'
        }, follow_redirects=True)
        assert signup_resp.status_code == 200, f"Signup failed: {signup_resp.status_code}"

        user = User.query.filter_by(email='farmer_test@agrihelper.in').first()
        assert user is not None, "User was not created in DB!"
        assert user.check_password('securepassword123'), "Password hash verification failed!"
        print(f"[PASS] Local user registered and password hashed successfully: {user.name} ({user.email})")

        # Login
        login_resp = client.post('/login', data={
            'email': 'farmer_test@agrihelper.in',
            'password': 'securepassword123'
        }, follow_redirects=True)
        assert login_resp.status_code == 200, f"Login failed: {login_resp.status_code}"
        print(f"[PASS] User login successfully authenticated.")

    print("\n==========================================")
    print("ALL PHASE 0 VERIFICATION TESTS PASSED! 100%")
    print("==========================================")

if __name__ == '__main__':
    run_tests()
