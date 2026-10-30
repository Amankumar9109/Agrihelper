from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True, index=True)
    provider = db.Column(db.String(20), default='local')  # 'local' or 'google'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_scheme_check = db.Column(db.DateTime, nullable=True)

    # Relationships
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
