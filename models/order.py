from datetime import datetime
from extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    razorpay_order_id = db.Column(db.String(100), nullable=True, unique=True)
    razorpay_payment_id = db.Column(db.String(100), nullable=True)
    razorpay_signature = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='pending')  # pending, paid, failed, delivered
    shipping_address = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'razorpay_order_id': self.razorpay_order_id,
            'razorpay_payment_id': self.razorpay_payment_id,
            'amount': self.amount,
            'status': self.status,
            'shipping_address': self.shipping_address,
            'phone_number': self.phone_number,
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p'),
            'items': [item.to_dict() for item in self.items.all()]
        }

    def __repr__(self):
        return f'<Order {self.id} status={self.status} amount={self.amount}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'price': self.price,
            'quantity': self.quantity,
            'subtotal': round(self.price * self.quantity, 2)
        }

    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'
