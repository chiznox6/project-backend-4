from . import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    quantity = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="cart_items")
    product = db.relationship("Product", back_populates="cart_items")

    __table_args__ = (db.UniqueConstraint("user_id", "product_id", name="_user_product_uc"),)
