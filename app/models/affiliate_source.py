from . import db

class AffiliateSource(db.Model):
    __tablename__ = "affiliate_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    api_name = db.Column(db.String(100))
    base_url = db.Column(db.Text)

    products = db.relationship("Product", back_populates="affiliate_source", cascade="all, delete-orphan")
