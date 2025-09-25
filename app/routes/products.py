from flask import Blueprint, request, jsonify
from app.models import db, Product
from app.schemas import ProductSchema

product_bp = Blueprint("products", __name__, url_prefix="/products")
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# GET all products
@product_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products), 200

# GET single product
@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product), 200

# POST new product
@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.get_json()
    errors = product_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

# PATCH product
@product_bp.route("/<int:id>", methods=["PATCH"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    errors = product_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return product_schema.jsonify(product), 200

# DELETE product
@product_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
