import os
from datetime import datetime
from flask import render_template, request, jsonify, current_app
from flask_login import current_user
from extensions import db
from models.chat import ChatMessage
from . import chatbot_bp
from .rag_engine import RAGEngine

# Global singleton RAG engine instance
_rag_engine = None

def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        kb_path = os.path.join(current_app.root_path, 'static', 'data', 'knowledge_base')
        _rag_engine = RAGEngine(knowledge_dir=kb_path)
        _rag_engine.load_and_index()
    return _rag_engine

@chatbot_bp.route('/chat')
@chatbot_bp.route('/kisanmitra')
def chat_page():
    """Renders the dedicated full-page KisanMitra AI Chat Advisor interface."""
    initial_prompt = request.args.get('q', '').strip()
    return render_template('chat.html', initial_prompt=initial_prompt)

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    """RAG query endpoint: processes user question and returns reply + sources."""
    data = request.get_json() or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Message cannot be empty.'}), 400

    engine = get_rag_engine()
    result = engine.query(message)
    reply = result['reply']
    sources = result['sources']
    source_links = result.get('source_links', [])

    # Persist in database if user is authenticated
    if current_user.is_authenticated:
        try:
            chat_record = ChatMessage(
                user_id=current_user.id,
                question=message,
                answer=reply,
                sources=", ".join(sources) if sources else ""
            )
            db.session.add(chat_record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.warning(f"Failed to save chat message: {e}")

    return jsonify({
        'reply': reply,
        'sources': sources,
        'source_links': source_links,
        'timestamp': datetime.utcnow().strftime('%H:%M')
    })

@chatbot_bp.route('/api/chat/history', methods=['GET'])
def chat_history():
    """Returns conversation history for logged in user."""
    if not current_user.is_authenticated:
        return jsonify({'history': []})

    messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.created_at.asc()).limit(30).all()
    return jsonify({
        'history': [m.to_dict() for m in messages]
    })

@chatbot_bp.route('/api/chat/clear', methods=['POST'])
def clear_history():
    """Clears conversation history for the current user."""
    if not current_user.is_authenticated:
        return jsonify({'success': True})

    try:
        ChatMessage.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/api/chat/suggested', methods=['GET'])
def suggested_prompts():
    """Returns seasonal and categorized prompts for farmer quick-actions."""
    categories = [
        {
            "category": "Govt Schemes & Subsidies",
            "icon": "fa-landmark",
            "prompts": [
                "What is PM-KISAN and how to complete eKYC for installment?",
                "How to report localized crop loss under PMFBY within 72 hours?",
                "What is the interest subvention rate on Kisan Credit Card (KCC)?"
            ]
        },
        {
            "category": "Modern Precision Techniques",
            "icon": "fa-tractor",
            "prompts": [
                "How does drip irrigation save 60% water and what subsidy is offered under PMKSY?",
                "What are the benefits of Kisan Drones for pesticide spraying?",
                "How do I set up a commercial hydroponic NFT system for tomatoes?"
            ]
        },
        {
            "category": "Crop Sowing & Fertilizers",
            "icon": "fa-seedling",
            "prompts": [
                "What is the critical irrigation schedule and NPK dosage for Wheat?",
                "What is the difference between Urea, DAP, and MOP fertilizers?",
                "How to cure tomato leaf curl and manage whitefly vector organically?"
            ]
        },
        {
            "category": "Mandi Prices & Markets",
            "icon": "fa-chart-line",
            "prompts": [
                "What is the difference between MSP and APMC Mandi Modal Price?",
                "How does the e-NAM electronic portal help farmers get better prices?"
            ]
        }
    ]
    return jsonify({
        'success': True,
        'suggestions': categories
    })
