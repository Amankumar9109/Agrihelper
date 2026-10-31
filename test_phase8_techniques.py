"""
Test Suite: Enhanced Modern Farming Techniques System
Verifies:
- /techniques hub with categories and search filtering
- /techniques/<slug> dynamic modern detail pages
- Backward compatibility routes (/modern_farming/...)
- REST API endpoints (/api/techniques, /api/techniques/<slug>, /api/techniques/calculate-roi)
- Interactive ROI & water savings calculation logic
"""

import sys
from app import create_app

def run_techniques_test():
    app = create_app('testing')
    client = app.test_client()

    print("========================================")
    print("Starting Modern Farming Techniques Test Suite")
    print("========================================")

    with app.app_context():
        # 1. Main Hub
        res = client.get('/techniques')
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert "Modern Farming Techniques" in html
        assert "Smart Farming ROI & Savings Calculator" in html
        assert "Precision Drip Irrigation" in html
        assert "Agricultural Drones" in html
        assert "Hydroponics" in html
        assert "Vertical Farming" in html
        assert "Solar-Powered Smart Agriculture" in html
        print("[OK] GET /techniques rendered modern hub with calculator and full technique catalog")

        # 2. Category Filtering
        res = client.get('/techniques?category=Clean%20Energy')
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert "Solar-Powered Smart Agriculture" in html
        print("[OK] GET /techniques?category=Clean Energy filtered catalog accurately")

        # 3. Search Query
        res = client.get('/techniques?q=drone')
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert "Agricultural Drones" in html
        assert "Precision Spraying" in html
        print("[OK] GET /techniques?q=drone returned matching drone technique")

        # 4. Dynamic Detail Page
        res = client.get('/techniques/drip-irrigation')
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert "Precision Drip Irrigation" in html
        assert "Step-by-Step Implementation Guide" in html
        assert "Govt Subsidies" in html
        assert "PMKSY" in html
        print("[OK] GET /techniques/drip-irrigation rendered rich detail view with subsidy & store kits")

        # 5. Other Dynamic Slugs
        for slug in ['solar-smart-farming', 'vertical-farming', 'hydroponics', 'ai-data-analytics', 'greenhouse-polyhouse']:
            res = client.get(f'/techniques/{slug}')
            assert res.status_code == 200
        print("[OK] All dynamic technique detail slugs rendered with status 200 OK")

        # 6. Backward Compatibility Routes
        legacy_checks = [
            ('/modern_farming/drip_irrigation', 'Drip Irrigation'),
            ('/modern_farming/soil_health', 'Soil Health'),
            ('/modern_farming/vertical_farming', 'Vertical Farming'),
            ('/modern_farming/drones_agriculture', 'Drones Agriculture'),
            ('/modern_farming/hydroponics', 'Hydroponics'),
            ('/modern_farming/ai_data_analytics', 'AI & Data Analytics')
        ]
        for route, phrase in legacy_checks:
            res = client.get(route)
            assert res.status_code == 200
            assert phrase in res.data.decode('utf-8')
        print("[OK] All 6 legacy /modern_farming/* routes verified (200 OK & exact test phrases)")

        # 7. JSON API - All Techniques
        res = client.get('/api/techniques')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert data['count'] >= 9
        assert len(data['techniques']) >= 9
        print(f"[OK] GET /api/techniques returned {data['count']} techniques in JSON")

        # 8. JSON API - Filter by Category
        res = client.get('/api/techniques?category=Water%20Management')
        assert res.status_code == 200
        data = res.get_json()
        assert any(t['slug'] == 'drip-irrigation' for t in data['techniques'])
        print("[OK] GET /api/techniques?category=Water Management returned filtered JSON")

        # 9. JSON API - Single Technique
        res = client.get('/api/techniques/drones-agriculture')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert data['technique']['title'] == "Agricultural Drones & Precision Spraying"
        assert data['technique']['subsidy_code'] == "SMAM"
        print("[OK] GET /api/techniques/drones-agriculture returned single technique details")

        # 10. JSON API - 404 for invalid technique
        res = client.get('/api/techniques/invalid-technique-xyz')
        assert res.status_code == 404
        print("[OK] GET /api/techniques/invalid-technique-xyz correctly returned 404")

        # 11. POST /api/techniques/calculate-roi
        calc_payload = {
            "technique": "drip-irrigation",
            "acres": 2.5,
            "crop": "Sugarcane"
        }
        res = client.post('/api/techniques/calculate-roi', json=calc_payload)
        assert res.status_code == 200
        calc_data = res.get_json()
        assert calc_data['success'] is True
        d = calc_data['data']
        assert d['farm_acres'] == 2.5
        assert d['base_setup_cost'] > 0
        assert d['estimated_subsidy'] > 0
        assert d['water_saved_liters'] > 1000000
        assert d['net_farmer_cost'] < d['base_setup_cost']
        assert "months" in d['payback_period'] or "years" in d['payback_period']
        print(f"[OK] POST /api/techniques/calculate-roi: 2.5 Acres Sugarcane Drip -> Water Saved: {d['water_saved_liters']:,} L, Subsidy: Rs.{d['estimated_subsidy']:,}, Payback: {d['payback_period']}")

    print("========================================")
    print("ALL MODERN FARMING TECHNIQUES TESTS PASSED (11/11)!")
    print("========================================")

if __name__ == '__main__':
    run_techniques_test()
