from datetime import datetime
from extensions import db

class GovernmentScheme(db.Model):
    __tablename__ = 'government_schemes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, index=True)
    code = db.Column(db.String(50), unique=True, nullable=True) # e.g. PM-KISAN, PMFBY, eNAM
    category = db.Column(db.String(60), nullable=False, index=True) # financial, insurance, market, credit, irrigation, organic
    tagline = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.Text, nullable=False)
    documents_required = db.Column(db.Text, nullable=True)
    how_to_apply = db.Column(db.Text, nullable=False)
    official_url = db.Column(db.String(350), nullable=False)
    nodal_ministry = db.Column(db.String(200), default="Ministry of Agriculture & Farmers Welfare")
    badge = db.Column(db.String(50), nullable=True) # e.g. "Direct DBT", "Popular", "Govt Subsidy", "New"
    legacy_route = db.Column(db.String(50), nullable=True) # e.g. "policy.p1"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'category': self.category,
            'tagline': self.tagline,
            'description': self.description,
            'benefits': self.benefits,
            'eligibility': self.eligibility,
            'documents_required': self.documents_required,
            'how_to_apply': self.how_to_apply,
            'official_url': self.official_url,
            'nodal_ministry': self.nodal_ministry,
            'badge': self.badge,
            'legacy_route': self.legacy_route,
            'is_active': self.is_active,
            'last_updated': self.last_updated.strftime('%d %b %Y') if self.last_updated else ''
        }

    def __repr__(self):
        return f'<GovernmentScheme {self.code or self.name}>'
