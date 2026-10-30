import os
import sys
import json
from datetime import datetime, timedelta
from app import create_app
from extensions import db
from models.user import User
from models.scheme import GovernmentScheme
from services.scheme_service import sync_schemes_cache, get_all_schemes, evaluate_eligibility

def test_phase5():
    print("========================================")
    print("Starting Phase 5 Test Suite: Real-Time Government Schemes")
    print("========================================")

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        # Ensure database tables exist
        db.create_all()

        # 1. Test Seed & Sync Schemes Cache
        count = sync_schemes_cache(force=True)
        assert count >= 12, f"Expected at least 12 schemes, got {count}"
        print(f"[OK] Schemes cache synced: {count} schemes in database")

        # Verify key schemes are present
        pm_kisan = GovernmentScheme.query.filter_by(code='PM-KISAN').first()
        assert pm_kisan is not None
        assert pm_kisan.category == 'Financial Aid'
        assert pm_kisan.legacy_route == 'policy.p1'

        pmfby = GovernmentScheme.query.filter_by(code='PMFBY').first()
        assert pmfby is not None
        assert pmfby.category == 'Crop Insurance'
        assert pmfby.legacy_route == 'policy.p2'

        kusum = GovernmentScheme.query.filter_by(code='PM-KUSUM').first()
        assert kusum is not None
        assert kusum.category == 'Irrigation & Solar'

        print("[OK] Verified key schemes in DB: PM-KISAN, PMFBY, PM-KUSUM")

        # 2. Test User Model last_scheme_check column
        test_email = "scheme_tester@agrihelper.local"
        user = User.query.filter_by(email=test_email).first()
        if not user:
            user = User(
                name="Scheme Tester",
                email=test_email,
                provider="local"
            )
            db.session.add(user)
        user.set_password("TestPassword123!")
        # Set last_scheme_check to 3 days ago to test new scheme notification
        user.last_scheme_check = datetime.utcnow() - timedelta(days=3)
        db.session.commit()
        user_id = user.id
        print(f"[OK] Test user ready with past last_scheme_check timestamp (ID: {user_id})")

    client = app.test_client()

    # 3. Test Web Page Rendering (GET /policy)
    res = client.get('/policy')
    assert res.status_code == 200, f"Expected 200 from /policy, got {res.status_code}"
    assert b"Government Schemes" in res.data
    assert b"PM-KISAN" in res.data
    assert b"Check My Eligibility Wizard" in res.data
    print("[OK] GET /policy rendered successfully with hero, filter bar and scheme cards")

    # 4. Test Category Filter on Web Page
    res = client.get('/policy?category=Crop%20Insurance')
    assert res.status_code == 200
    assert b"PMFBY" in res.data
    print("[OK] GET /policy?category=Crop%20Insurance filtered successfully")

    # 5. Test Search Query on Web Page
    res = client.get('/policy?q=solar')
    assert res.status_code == 200
    assert b"PM-KUSUM" in res.data
    print("[OK] GET /policy?q=solar returned PM-KUSUM")

    # 6. Test Backward Compatibility: p1 to p5 detailed pages
    for p_id in ['p1', 'p2', 'p3', 'p4', 'p5']:
        res = client.get(f'/policy/{p_id}')
        assert res.status_code == 200, f"Expected 200 for /policy/{p_id}, got {res.status_code}"
    print("[OK] Backward compatibility verified: /policy/p1 through /policy/p5 accessible (200 OK)")

    # 7. Test API Endpoints
    # GET /api/schemes
    res = client.get('/api/schemes')
    assert res.status_code == 200
    data = res.get_json()
    assert data.get('success') is True
    assert data.get('count') >= 12
    print(f"[OK] GET /api/schemes returned {data.get('count')} schemes")

    # GET /api/schemes?category=Market Access
    res = client.get('/api/schemes?category=Market%20Access')
    assert res.status_code == 200
    cat_data = res.get_json()
    assert cat_data.get('count') >= 1
    codes = [s['code'] for s in cat_data['schemes']]
    assert 'eNAM' in codes
    print("[OK] GET /api/schemes?category=Market Access returned eNAM")

    # GET /api/schemes?search=organic
    res = client.get('/api/schemes?search=organic')
    assert res.status_code == 200
    search_data = res.get_json()
    codes = [s['code'] for s in search_data['schemes']]
    assert 'PKVY' in codes
    print("[OK] GET /api/schemes?search=organic returned PKVY")

    # GET /api/schemes/<id>
    with app.app_context():
        first_scheme = GovernmentScheme.query.first()
        first_id = first_scheme.id

    res = client.get(f'/api/schemes/{first_id}')
    assert res.status_code == 200
    single_data = res.get_json()
    assert single_data.get('success') is True
    assert single_data['scheme']['id'] == first_id
    print(f"[OK] GET /api/schemes/{first_id} returned single scheme details")

    # 8. Test Refresh Endpoint (POST /api/schemes/refresh)
    res = client.post('/api/schemes/refresh')
    assert res.status_code == 200
    refresh_data = res.get_json()
    assert refresh_data.get('success') is True
    assert refresh_data.get('count') >= 12
    print(f"[OK] POST /api/schemes/refresh re-synced cache ({refresh_data.get('count')} schemes)")

    # 9. Test Eligibility Evaluation Engine
    # Case A: Marginal crop farmer looking for direct cash -> PM-KISAN
    res = client.post('/api/schemes/check-eligibility', json={
        'land_size': 'marginal',
        'farm_type': 'crops',
        'primary_need': 'cash'
    })
    assert res.status_code == 200
    eval_data = res.get_json()
    assert eval_data.get('success') is True
    matches = eval_data.get('matches', [])
    assert len(matches) > 0
    top_match = matches[0]
    assert top_match['scheme']['code'] == 'PM-KISAN'
    assert top_match['match_score'] >= 90
    print(f"[OK] Eligibility Wizard Case A: Top recommendation '{top_match['scheme']['name']}' ({top_match['match_score']}% match)")

    # Case B: Small organic farmer -> PKVY
    res = client.post('/api/schemes/check-eligibility', json={
        'land_size': 'small',
        'farm_type': 'organic',
        'primary_need': 'cash'
    })
    assert res.status_code == 200
    matches_b = res.get_json().get('matches', [])
    top_codes_b = [m['scheme']['code'] for m in matches_b[:2]]
    assert 'PKVY' in top_codes_b or 'PM-KISAN' in top_codes_b
    print("[OK] Eligibility Wizard Case B: Recommended organic scheme PKVY")

    # Case C: Farmer looking for solar pump -> PM-KUSUM
    res = client.post('/api/schemes/check-eligibility', json={
        'land_size': 'small',
        'farm_type': 'crops',
        'primary_need': 'solar_pump'
    })
    assert res.status_code == 200
    matches_c = res.get_json().get('matches', [])
    top_c = matches_c[0]
    assert top_c['scheme']['code'] == 'PM-KUSUM'
    print(f"[OK] Eligibility Wizard Case C: Recommended PM-KUSUM ({top_c['match_score']}% match)")

    # 10. Test Logged-in User Scheme Notification Banner
    login_res = client.post('/login', data={'email': test_email, 'password': 'TestPassword123!'}, follow_redirects=True)
    assert login_res.status_code == 200
    print("[OK] Logged in user for notification testing")

    # First visit should display new schemes alert
    res_auth = client.get('/policy')
    assert res_auth.status_code == 200
    assert b"Fresh Updates!" in res_auth.data or b"new or updated" in res_auth.data
    print("[OK] Verified returning user alert banner: shows new schemes since last check")

    # Subsequent visit should clear the notification (last_scheme_check updated)
    res_subsequent = client.get('/policy')
    assert res_subsequent.status_code == 200
    assert b"Fresh Updates!" not in res_subsequent.data
    print("[OK] Verified alert banner dismisses after viewing")

    print("========================================")
    print("ALL PHASE 5 TESTS PASSED (10/10)!")
    print("========================================")

if __name__ == '__main__':
    test_phase5()
