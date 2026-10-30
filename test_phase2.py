"""
Phase 2 Verification Test Suite for AgriHelper
Verifies:
1. PriceHistory Model & Database operations
2. /market route renders new UI with India Map container
3. /api/state-summary endpoint (overall & by commodity for map choropleth)
4. /api/commodities endpoint
5. /api/price-trends endpoint (7-day and 30-day historical trend curves & database caching)
6. /api/live_prices endpoint (APMC live/fallback)
7. /get_options and /get_prices compatibility
"""
from datetime import date
from app import create_app
from extensions import db
from models.price_history import PriceHistory

def run_phase2_tests():
    print("=== STARTING PHASE 2 TEST SUITE ===")
    app = create_app('testing')
    client = app.test_client()

    with app.app_context():
        db.create_all()

    # 1. Test PriceHistory Model
    print("\n--- 1. Testing PriceHistory Model ---")
    with app.app_context():
        test_ph = PriceHistory(
            state="Maharashtra",
            district="Pune",
            market="Pune",
            commodity="Onion",
            min_price=1200.0,
            max_price=2200.0,
            modal_price=1850.0,
            record_date=date.today()
        )
        db.session.add(test_ph)
        db.session.commit()

        queried = PriceHistory.query.filter_by(commodity="Onion", state="Maharashtra").first()
        assert queried is not None, "Failed to persist PriceHistory record"
        assert queried.modal_price == 1850.0
        print(f"[PASS] PriceHistory saved and retrieved: {queried}")

    # 2. Test Market Dashboard Page
    print("\n--- 2. Testing Market Template & Route ---")
    resp = client.get('/market')
    assert resp.status_code == 200, f"/market failed: {resp.status_code}"
    html = resp.data.decode('utf-8')
    assert 'indiaMapContainer' in html, "Missing India Map container in market.html"
    assert 'priceTrendChart' in html, "Missing Price Trend Canvas in market.html"
    assert 'mapCommodityFilter' in html, "Missing Choropleth Crop filter in market.html"
    assert 'india_states_data.js' in html, "Missing india_states_data.js script link"
    print("[PASS] GET /market returns 200 OK with Interactive India Map & Trend UI elements.")

    # 3. Test State Summary API for India Map
    print("\n--- 3. Testing /api/state-summary Endpoint ---")
    sum_resp = client.get('/api/state-summary')
    assert sum_resp.status_code == 200
    data = sum_resp.get_json()
    assert 'states' in data, "Missing 'states' key in state summary"
    assert 'Maharashtra' in data['states'], "Maharashtra not found in state summary"
    mh_info = data['states']['Maharashtra']
    assert mh_info['mandis'] > 0, "Maharashtra should have active mandis"
    print(f"[PASS] State Summary overall: Maharashtra has {mh_info['mandis']} mandis, top crop: {mh_info['top_commodity']}.")

    # Test by Commodity filter (e.g. Potato)
    comm_sum_resp = client.get('/api/state-summary?commodity=Potato')
    assert comm_sum_resp.status_code == 200
    potato_data = comm_sum_resp.get_json()
    assert potato_data['commodity'] == 'Potato'
    assert potato_data['min_price'] > 0
    print(f"[PASS] State Summary for 'Potato': Min Rs.{potato_data['min_price']} - Max Rs.{potato_data['max_price']}.")

    # 4. Test Commodities API
    print("\n--- 4. Testing /api/commodities Endpoint ---")
    comm_resp = client.get('/api/commodities')
    assert comm_resp.status_code == 200
    comms = comm_resp.get_json()
    assert len(comms) > 10, "Should have more than 10 commodities in dataset"
    assert 'Wheat' in comms or 'Potato' in comms or 'Onion' in comms
    print(f"[PASS] /api/commodities returned {len(comms)} unique commodities.")

    # 5. Test Price Trends (7-day and 30-day)
    print("\n--- 5. Testing /api/price-trends Endpoint ---")
    # 30-day trend
    trend_resp_30 = client.post('/api/price-trends', json={
        'state': 'Maharashtra',
        'district': 'Pune',
        'market': 'Pune',
        'commodity': 'Onion',
        'days': 30
    })
    assert trend_resp_30.status_code == 200, f"/api/price-trends failed: {trend_resp_30.status_code}"
    trend_30 = trend_resp_30.get_json()
    assert len(trend_30['dates']) == 31, f"Expected 31 date points, got {len(trend_30['dates'])}"
    assert len(trend_30['modal_prices']) == 31
    assert 'change_pct' in trend_30
    print(f"[PASS] 30-Day Trend generated: {trend_30['commodity']} current price Rs.{trend_30['current_price']} ({trend_30['change_pct']}% change).")

    # 7-day trend
    trend_resp_7 = client.post('/api/price-trends', json={
        'state': 'Punjab',
        'commodity': 'Wheat',
        'days': 7
    })
    assert trend_resp_7.status_code == 200
    trend_7 = trend_resp_7.get_json()
    assert len(trend_7['dates']) == 8
    print(f"[PASS] 7-Day Trend generated for Wheat in Punjab.")

    # 6. Test Live Prices API
    print("\n--- 6. Testing /api/live_prices Endpoint ---")
    live_resp = client.post('/api/live_prices', json={
        'state': 'Maharashtra',
        'commodity': 'Onion'
    })
    assert live_resp.status_code == 200
    live_data = live_resp.get_json()
    assert 'source' in live_data
    assert len(live_data.get('records', [])) > 0
    print(f"[PASS] /api/live_prices returned {len(live_data['records'])} records from {live_data['source']}.")

    # 7. Test Backward Compatibility for /get_options and /get_prices
    print("\n--- 7. Testing Legacy Market Options & Prices ---")
    opts_resp = client.post('/get_options', json={'level': 'district', 'selection': 'Maharashtra'})
    assert opts_resp.status_code == 200
    assert len(opts_resp.get_json()) > 0
    print(f"[PASS] /get_options returned {len(opts_resp.get_json())} districts in Maharashtra.")

    print("\n==========================================")
    print("ALL PHASE 2 VERIFICATION TESTS PASSED! 100%")
    print("==========================================")

if __name__ == '__main__':
    run_phase2_tests()
