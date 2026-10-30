from datetime import datetime
from extensions import db

class PostLike(db.Model):
    __tablename__ = 'post_likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
    )

    def __repr__(self):
        return f'<PostLike user={self.user_id} post={self.post_id}>'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='Discussion')  # Discussion, Questions, Tips, Success Stories
    image_url = db.Column(db.String(300), nullable=True)
    upvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan', order_by='Comment.created_at.asc()')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def is_liked_by(self, user_id):
        if not user_id:
            return False
        return self.likes.filter_by(user_id=user_id).first() is not None

    def get_likes_count(self):
        return self.likes.count()

    def to_dict(self, current_user_id=None):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'image_url': self.image_url,
            'author_name': self.author.name if self.author else 'Community Member',
            'author_avatar': self.author.avatar_url if (self.author and self.author.avatar_url) else 'https://ui-avatars.com/api/?name=Farmer&background=15803d&color=fff',
            'likes_count': self.likes.count(),
            'comments_count': self.comments.count(),
            'is_liked': self.is_liked_by(current_user_id) if current_user_id else False,
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p')
        }

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author_name': self.author.name if self.author else 'Farmer',
            'author_avatar': self.author.avatar_url if (self.author and self.author.avatar_url) else 'https://ui-avatars.com/api/?name=Farmer&background=15803d&color=fff',
            'content': self.content,
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p')
        }

    def __repr__(self):
        return f'<Comment {self.id} on post {self.post_id}>'
