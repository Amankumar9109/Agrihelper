from datetime import datetime, date
from extensions import db

class PriceHistory(db.Model):
    __tablename__ = 'price_history'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False, index=True)
    district = db.Column(db.String(100), nullable=False)
    market = db.Column(db.String(100), nullable=False, index=True)
    commodity = db.Column(db.String(100), nullable=False, index=True)
    min_price = db.Column(db.Float, nullable=False)
    max_price = db.Column(db.Float, nullable=False)
    modal_price = db.Column(db.Float, nullable=False)
    record_date = db.Column(db.Date, default=date.today, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'district': self.district,
            'market': self.market,
            'commodity': self.commodity,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'modal_price': self.modal_price,
            'record_date': self.record_date.isoformat() if self.record_date else None
        }

    def __repr__(self):
        return f'<PriceHistory {self.commodity} in {self.market} on {self.record_date}: Rs.{self.modal_price}>'
