from . import db

class AffiliateSource(db.Model):
    __tablename__ = "affiliate_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True, index=True)
    api_name = db.Column(db.String(150), nullable=True)
    base_url = db.Column(db.String(2048), nullable=True)

    # Relationships
    products = db.relationship(
        "Product",
        back_populates="affiliate_source",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<AffiliateSource id={self.id}, name={self.name}>"
