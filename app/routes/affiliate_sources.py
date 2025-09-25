from flask import Blueprint, request, jsonify
from app.models import db, AffiliateSource
from app.schemas import AffiliateSourceSchema

affiliate_bp = Blueprint("affiliate_sources", __name__, url_prefix="/affiliate-sources")
affiliate_schema = AffiliateSourceSchema()
affiliates_schema = AffiliateSourceSchema(many=True)

# GET all affiliate sources
@affiliate_bp.route("/", methods=["GET"])
def get_affiliate_sources():
    affiliates = AffiliateSource.query.all()
    return affiliates_schema.jsonify(affiliates), 200

# GET single affiliate source
@affiliate_bp.route("/<int:id>", methods=["GET"])
def get_affiliate_source(id):
    affiliate = AffiliateSource.query.get_or_404(id)
    return affiliate_schema.jsonify(affiliate), 200

# POST new affiliate source
@affiliate_bp.route("/", methods=["POST"])
def create_affiliate_source():
    data = request.get_json()
    errors = affiliate_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    affiliate = AffiliateSource(**data)
    db.session.add(affiliate)
    db.session.commit()
    return affiliate_schema.jsonify(affiliate), 201

# PATCH affiliate source
@affiliate_bp.route("/<int:id>", methods=["PATCH"])
def update_affiliate_source(id):
    affiliate = AffiliateSource.query.get_or_404(id)
    data = request.get_json()
    errors = affiliate_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(affiliate, key, value)
    db.session.commit()
    return affiliate_schema.jsonify(affiliate), 200

# DELETE affiliate source
@affiliate_bp.route("/<int:id>", methods=["DELETE"])
def delete_affiliate_source(id):
    affiliate = AffiliateSource.query.get_or_404(id)
    db.session.delete(affiliate)
    db.session.commit()
    return jsonify({"message": "Affiliate source deleted"}), 200
