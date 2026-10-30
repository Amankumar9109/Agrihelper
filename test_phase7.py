import os
import sys
import json
from app import create_app
from extensions import db

def test_phase7():
    print("========================================")
    print("Starting Phase 7 Test Suite: Polish, Security & Deployment")
    print("========================================")

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    client = app.test_client()

    # 1. Test Secure Weather Proxy Endpoint (GET /api/weather)
    res = client.get('/api/weather?city=Pune')
    assert res.status_code == 200, f"Expected 200 from /api/weather, got {res.status_code}"
    w_data = res.get_json()
    assert 'current' in w_data
    assert 'location' in w_data
    assert 'agri_advisory' in w_data
    assert 'history_7days' in w_data
    assert len(w_data['history_7days']) == 7
    advisory = w_data['agri_advisory']
    assert 'spraying_safe' in advisory
    assert 'irrigation_needed' in advisory
    print(f"[OK] GET /api/weather?city=Pune returned weather data and agricultural advisory")

    # Test another city
    res_nashik = client.get('/api/weather?city=Nashik')
    assert res_nashik.status_code == 200
    n_data = res_nashik.get_json()
    assert n_data['location']['name'].lower() == 'nashik'
    print("[OK] GET /api/weather?city=Nashik returned city-specific data via secure proxy")

    # Test Weather HTML Page
    res_w_html = client.get('/weather')
    assert res_w_html.status_code == 200
    assert b"Farm Weather & Spray Advisory" in res_w_html.data
    assert b"Secure Proxy Active" in res_w_html.data
    print("[OK] GET /weather rendered modern weather page extending base.html")

    # 2. Test Custom 404 Error Page & JSON API handling
    res_404_html = client.get('/this-route-does-not-exist-at-all')
    assert res_404_html.status_code == 404
    assert b"Field Not Found!" in res_404_html.data or b"404" in res_404_html.data
    print("[OK] Custom 404 HTML error page rendered successfully")

    res_404_api = client.get('/api/non-existent-endpoint')
    assert res_404_api.status_code == 404
    api_err = res_404_api.get_json()
    assert api_err.get('status_code') == 404
    assert 'error' in api_err
    print("[OK] Custom 404 API endpoint returned structured JSON error")

    # 3. Test SEO Meta Tags & Open Graph
    res_home = client.get('/')
    assert res_home.status_code == 200
    assert b'name="description"' in res_home.data
    assert b'property="og:title"' in res_home.data
    assert b'property="og:image"' in res_home.data
    assert b'name="twitter:card"' in res_home.data
    print("[OK] SEO & Open Graph social sharing meta tags verified on base template")

    # 4. Test UI/UX Polish: Theme Toggle & Toast Notifications
    assert b'id="themeToggleBtn"' in res_home.data
    assert b'id="agriToast"' in res_home.data
    assert b'showToast' in res_home.data
    assert b'skeleton' in res_home.data
    print("[OK] Global theme toggle, toast notification container, and skeleton animations present")

    # 5. Test Deployment Configuration Files
    root_dir = app.root_path
    
    procfile = os.path.join(root_dir, 'Procfile')
    assert os.path.exists(procfile), "Procfile is missing"
    with open(procfile, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'web: gunicorn' in content and 'app:create_app()' in content
    print("[OK] Procfile verified: configured for production gunicorn")

    runtime_file = os.path.join(root_dir, 'runtime.txt')
    assert os.path.exists(runtime_file), "runtime.txt is missing"
    with open(runtime_file, 'r', encoding='utf-8') as f:
        r_content = f.read()
    assert 'python-' in r_content
    print(f"[OK] runtime.txt verified: {r_content.strip()}")

    env_ex = os.path.join(root_dir, '.env.example')
    assert os.path.exists(env_ex), ".env.example is missing"
    print("[OK] .env.example configuration template verified")

    req_file = os.path.join(root_dir, 'requirements.txt')
    with open(req_file, 'r', encoding='utf-8') as f:
        reqs = f.read()
    assert 'gunicorn' in reqs
    print("[OK] requirements.txt includes gunicorn for production WSGI server")

    print("========================================")
    print("ALL PHASE 7 TESTS PASSED (10/10)!")
    print("========================================")

if __name__ == '__main__':
    test_phase7()
