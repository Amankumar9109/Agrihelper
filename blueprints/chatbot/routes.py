from flask import jsonify, request
from . import chatbot_bp

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    # Phase 3 stub - RAG engine integration
    return jsonify({
        'reply': f"Hello from AgriBot! I received your question: '{message}'. The full RAG intelligence will be connected in Phase 3.",
        'sources': []
    })
