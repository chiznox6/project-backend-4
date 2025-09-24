from . import db
from sqlalchemy import Index
from decimal import Decimal

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    image_url = db.Column(db.String(2048), nullable=True)  # safer max length for URLs
    price = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    affiliate_link = db.Column(db.String(2048), nullable=False)
    affiliate_source_id = db.Column(
        db.Integer,
        db.ForeignKey("affiliate_sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Relationships
    affiliate_source = db.relationship("AffiliateSource", back_populates="products")
    cart_items = db.relationship("CartItem", back_populates="product", cascade="all, delete-orphan")

    # Optional: for debugging / easy printing
    def __repr__(self):
        return f"<Product id={self.id}, name={self.name}, price={self.price}>"
