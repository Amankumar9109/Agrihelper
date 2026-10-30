import os
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

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Message cannot be empty.'}), 400

    engine = get_rag_engine()
    result = engine.query(message)
    reply = result['reply']
    sources = result['sources']

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
        'sources': sources
    })

@chatbot_bp.route('/api/chat/history', methods=['GET'])
def chat_history():
    """Returns conversation history for logged in user"""
    if not current_user.is_authenticated:
        return jsonify({'history': []})

    messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.created_at.asc()).limit(30).all()
    return jsonify({
        'history': [m.to_dict() for m in messages]
    })

@chatbot_bp.route('/api/chat/clear', methods=['POST'])
def clear_history():
    """Clears conversation history for the current user"""
    if not current_user.is_authenticated:
        return jsonify({'success': True})

    try:
        ChatMessage.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
