"""
Phase 3 Comprehensive Verification Test Suite for AgriHelper
Verifies:
1. Knowledge base document indexing (NumPy-accelerated vector index)
2. RAG Semantic vector retrieval across English & Hinglish queries
3. /chat and /kisanmitra dedicated consultation pages
4. /api/chat POST endpoint returning agronomy answers & rich clickable citations
5. /api/chat/suggested endpoint returning categorized prompt chips
6. Chat history persistence for authenticated users
7. /api/chat/history and /api/chat/clear endpoints
8. Error handling for empty or malformed queries
"""
import os
from app import create_app
from extensions import db
from models.user import User
from models.chat import ChatMessage
from blueprints.chatbot.rag_engine import RAGEngine

def run_phase3_tests():
    print("=== STARTING PHASE 3 TEST SUITE ===")
    app = create_app('testing')
    client = app.test_client()

    with app.app_context():
        db.create_all()

    # 1. Test RAG Engine Direct Indexing
    print("\n--- 1. Testing RAG Engine Indexing & Chunks ---")
    kb_path = os.path.join(app.root_path, 'static', 'data', 'knowledge_base')
    engine = RAGEngine(knowledge_dir=kb_path)
    engine.load_and_index()

    assert engine.num_chunks >= 10, f"Expected at least 10 knowledge chunks, got {engine.num_chunks}"
    assert len(engine.vocabulary) > 50, f"Vocabulary too small: {len(engine.vocabulary)}"
    print(f"[PASS] RAG Engine loaded {engine.num_chunks} chunks with {len(engine.vocabulary)} vocabulary terms.")

    # 2. Test Semantic Retrieval Accuracy
    print("\n--- 2. Testing Semantic Retrieval Accuracy ---")
    test_queries = [
        ("PM KISAN financial benefit installments", "government_schemes.txt"),
        ("drip irrigation water savings and subsidy", "farming_techniques.txt"),
        ("Wheat sowing time and critical irrigation stages", "crop_calendar.txt"),
        ("Kisan Call Center toll free helpline number", "faq.txt"),
        ("APMC modal price and MSP commodities", "market_guide.txt"),
        ("gehu me kitna paani de", "crop_calendar.txt"),
        ("tomato leaf curl kitnashak neem spray", "faq.txt")
    ]

    for q, expected_source in test_queries:
        retrieved = engine.retrieve(q, top_k=3)
        assert len(retrieved) > 0, f"No chunks retrieved for: {q}"
        sources = [c['source'] for c in retrieved]
        assert expected_source in sources, f"Expected {expected_source} in {sources} for query: {q}"
        print(f"[PASS] Query '{q[:35]}...' -> Retrieved from {expected_source}")

    # 3. Test Dedicated Chat Routes
    print("\n--- 3. Testing Dedicated Full-Page Chat Routes ---")
    res_chat = client.get('/chat')
    assert res_chat.status_code == 200
    assert "KisanMitra" in res_chat.data.decode('utf-8')
    assert "Curated Advisory Topics" in res_chat.data.decode('utf-8')

    res_km = client.get('/kisanmitra')
    assert res_km.status_code == 200
    print("[PASS] GET /chat and /kisanmitra rendered full-page consultation room (200 OK).")

    # 4. Test /api/chat/suggested Endpoint
    print("\n--- 4. Testing /api/chat/suggested Endpoint ---")
    sugg_resp = client.get('/api/chat/suggested')
    assert sugg_resp.status_code == 200
    sugg_data = sugg_resp.get_json()
    assert sugg_data['success'] is True
    assert len(sugg_data['suggestions']) >= 4
    print(f"[PASS] /api/chat/suggested returned {len(sugg_data['suggestions'])} categorized prompt bundles.")

    # 5. Test /api/chat Endpoint
    print("\n--- 5. Testing /api/chat Endpoint ---")
    # Empty message validation
    empty_resp = client.post('/api/chat', json={'message': '   '})
    assert empty_resp.status_code == 400
    print("[PASS] Empty message rejected with 400 Bad Request.")

    # Valid agronomy query
    chat_resp = client.post('/api/chat', json={
        'message': 'What is the financial assistance provided under PM-KISAN?'
    })
    assert chat_resp.status_code == 200, f"/api/chat failed: {chat_resp.status_code}"
    data = chat_resp.get_json()
    assert 'reply' in data and len(data['reply']) > 40
    assert 'sources' in data and len(data['sources']) > 0
    assert 'government_schemes.txt' in data['sources']
    assert 'source_links' in data and len(data['source_links']) > 0
    assert any(s['url'] == '/policy' for s in data['source_links'])
    print(f"[PASS] /api/chat replied ({len(data['reply'])} chars) with sources & rich links: {[s['name'] for s in data['source_links']]}")

    # 6. Test Chat History Persistence with Authenticated User
    print("\n--- 6. Testing Chat History with Authenticated User ---")
    with app.app_context():
        # Setup test user
        user = User.query.filter_by(email='rag_farmer@agrihelper.in').first()
        if not user:
            user = User(name='RAG Farmer', email='rag_farmer@agrihelper.in', provider='local')
            user.set_password('FarmerPass2026!')
            db.session.add(user)
            db.session.commit()
        user_id = user.id

    # Log in
    client.post('/login', data={'email': 'rag_farmer@agrihelper.in', 'password': 'FarmerPass2026!'}, follow_redirects=True)

    # Send chat while logged in
    auth_chat_resp = client.post('/api/chat', json={
        'message': 'How does drip irrigation help save water?'
    })
    assert auth_chat_resp.status_code == 200

    # Verify message was saved to database
    with app.app_context():
        saved_msg = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at.desc()).first()
        assert saved_msg is not None, "ChatMessage was not saved to database!"
        assert "drip irrigation" in saved_msg.question.lower()
        assert "farming_techniques.txt" in saved_msg.sources
        print(f"[PASS] ChatMessage persisted in database: Q: '{saved_msg.question}' | Sources: {saved_msg.sources}")

    # Test /api/chat/history
    hist_resp = client.get('/api/chat/history')
    assert hist_resp.status_code == 200
    history = hist_resp.get_json().get('history', [])
    assert len(history) >= 1
    print(f"[PASS] /api/chat/history returned {len(history)} past messages for logged in user.")

    # Test /api/chat/clear
    clear_resp = client.post('/api/chat/clear')
    assert clear_resp.status_code == 200
    with app.app_context():
        remaining = ChatMessage.query.filter_by(user_id=user_id).count()
        assert remaining == 0, f"Expected 0 messages after clear, found {remaining}"
    print("[PASS] /api/chat/clear successfully cleared conversation history.")

    print("\n==========================================")
    print("ALL PHASE 3 VERIFICATION TESTS PASSED! 100%")
    print("==========================================")

if __name__ == '__main__':
    run_phase3_tests()
