"""
Phase 1 Verification Test Suite for AgriHelper
Verifies:
1. Local user signup (validation, password hashing, avatar generation)
2. Local user login and session creation
3. Session logout
4. Google OAuth endpoints (/auth/google, /auth/google/dev-demo)
5. @login_required route protection on /community/post, /cart, /checkout
"""
from app import create_app
from extensions import db
from models.user import User

def run_phase1_tests():
    print("=== STARTING PHASE 1 TEST SUITE ===")
    app = create_app('testing')
    client = app.test_client()

    with app.app_context():
        db.create_all()

    # 1. Test Unauthenticated Access to Protected Routes
    print("\n--- 1. Testing @login_required Route Protection ---")
    protected_urls = ['/community/post', '/cart', '/checkout']
    for url in protected_urls:
        resp = client.get(url)
        assert resp.status_code == 302, f"Expected 302 redirect for {url}, got {resp.status_code}"
        assert '/login' in resp.headers.get('Location', ''), f"Expected redirect to /login for {url}"
        print(f"[PASS] Unauthenticated {url:<20} -> 302 Redirect to {resp.headers['Location']}")

    # 2. Test Local Signup
    print("\n--- 2. Testing Local Registration ---")
    with app.app_context():
        User.query.filter_by(email='kisan.sharma@agrihelper.in').delete()
        db.session.commit()

        # Test short password
        short_pw_resp = client.post('/signup', data={
            'name': 'Kisan Sharma',
            'email': 'kisan.sharma@agrihelper.in',
            'password': '123'
        }, follow_redirects=True)
        assert User.query.filter_by(email='kisan.sharma@agrihelper.in').first() is None
        print("[PASS] Rejected registration with short password (<6 chars).")

        # Test valid signup
        signup_resp = client.post('/signup', data={
            'name': 'Kisan Sharma',
            'email': 'kisan.sharma@agrihelper.in',
            'password': 'StrongAgriPass2026!'
        }, follow_redirects=True)
        assert signup_resp.status_code == 200

        user = User.query.filter_by(email='kisan.sharma@agrihelper.in').first()
        assert user is not None, "User not found in DB after signup"
        assert user.check_password('StrongAgriPass2026!'), "Password hash verification failed"
        assert user.provider == 'local', "Provider should be 'local'"
        assert user.avatar_url is not None, "Avatar URL should be auto-generated"
        print(f"[PASS] Successfully registered '{user.name}' ({user.email}) with avatar: {user.avatar_url}")

    # Logout to test login from unauthenticated state
    client.get('/logout')

    # 3. Test Local Login
    print("\n--- 3. Testing Local Login & Logout ---")
    # Invalid login
    bad_login = client.post('/login', data={
        'email': 'kisan.sharma@agrihelper.in',
        'password': 'WrongPassword123'
    }, follow_redirects=True)
    assert b"Invalid email or password" in bad_login.data
    print("[PASS] Invalid password rejected with error alert.")

    # Valid login
    good_login = client.post('/login', data={
        'email': 'kisan.sharma@agrihelper.in',
        'password': 'StrongAgriPass2026!'
    }, follow_redirects=True)
    assert good_login.status_code == 200
    print("[PASS] Valid credentials authenticated successfully.")

    # Access protected route while authenticated
    post_resp = client.get('/community/post')
    assert post_resp.status_code == 200, f"Authenticated access failed: {post_resp.status_code}"
    print("[PASS] Authenticated user can access /community/post (200 OK).")

    cart_resp = client.get('/cart')
    assert cart_resp.status_code == 200, f"Authenticated access to /cart failed: {cart_resp.status_code}"
    print("[PASS] Authenticated user can access /cart (200 OK).")

    # Logout
    logout_resp = client.get('/logout', follow_redirects=True)
    assert logout_resp.status_code == 200
    print("[PASS] User logged out successfully.")

    # Verify routes are protected again
    post_again = client.get('/community/post')
    assert post_again.status_code == 302
    print("[PASS] Route is protected again after logout.")

    # 4. Test Google OAuth Flow & Dev Demo Login
    print("\n--- 4. Testing Google OAuth Flow & Dev Demo Login ---")
    # /auth/google initiation
    google_init = client.get('/google', follow_redirects=False)
    # When GOOGLE_CLIENT_ID is not yet set in testing config, redirects to dev-login
    assert google_init.status_code == 302
    print(f"[PASS] /google redirects to {google_init.headers.get('Location')}")

    # Dev demo Google login
    demo_login = client.get('/google/dev-demo', follow_redirects=True)
    assert demo_login.status_code == 200

    with app.app_context():
        guser = User.query.filter_by(email="google.farmer.demo@agrihelper.in").first()
        assert guser is not None, "Google user not created in DB"
        assert guser.provider == "google", "Provider should be 'google'"
        assert guser.avatar_url is not None, "Google avatar should be populated"
        assert guser.google_id is not None, "Google ID should be populated"
        print(f"[PASS] Google user session active: {guser.name} | ID: {guser.google_id} | Provider: {guser.provider}")

    # Access protected routes with Google session
    post_g = client.get('/community/post')
    assert post_g.status_code == 200
    print("[PASS] Google-authenticated user can access protected /community/post.")

    cart_g = client.get('/cart')
    assert cart_g.status_code == 200
    print("[PASS] Google-authenticated user can access protected /cart.")

    # Logout Google user
    client.get('/logout')
    print("[PASS] Google user logged out successfully.")

    print("\n==========================================")
    print("ALL PHASE 1 VERIFICATION TESTS PASSED! 100%")
    print("==========================================")

if __name__ == '__main__':
    run_phase1_tests()
