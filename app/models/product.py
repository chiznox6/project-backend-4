from . import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2))
    affiliate_link = db.Column(db.Text, nullable=False)
    affiliate_source_id = db.Column(db.Integer, db.ForeignKey("affiliate_sources.id", ondelete="CASCADE"))

    affiliate_source = db.relationship("AffiliateSource", back_populates="products")
    cart_items = db.relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
