from datetime import datetime
from extensions import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    sources = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question': self.question,
            'answer': self.answer,
            'sources': self.sources.split(', ') if self.sources else [],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<ChatMessage {self.id} for user {self.user_id}>'
