from flask import Blueprint, request, jsonify
from app.models import db, CartItem
from app.schemas import CartItemSchema

cart_item_bp = Blueprint("cart_items", __name__, url_prefix="/cart-items")
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

# GET all cart items
@cart_item_bp.route("/", methods=["GET"])
def get_cart_items():
    cart_items = CartItem.query.all()
    return cart_items_schema.jsonify(cart_items), 200

# GET single cart item
@cart_item_bp.route("/<int:id>", methods=["GET"])
def get_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    return cart_item_schema.jsonify(cart_item), 200

# POST new cart item
@cart_item_bp.route("/", methods=["POST"])
def create_cart_item():
    data = request.get_json()
    errors = cart_item_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    cart_item = CartItem(**data)
    db.session.add(cart_item)
    db.session.commit()
    return cart_item_schema.jsonify(cart_item), 201

# PATCH cart item
@cart_item_bp.route("/<int:id>", methods=["PATCH"])
def update_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    data = request.get_json()
    errors = cart_item_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    for key, value in data.items():
        setattr(cart_item, key, value)
    db.session.commit()
    return cart_item_schema.jsonify(cart_item), 200

# DELETE cart item
@cart_item_bp.route("/<int:id>", methods=["DELETE"])
def delete_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Cart item deleted"}), 200
