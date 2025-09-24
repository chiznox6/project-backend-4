from flask import Blueprint, jsonify, request
from app.models.cart_item import CartItem
from app.models.user import User
from app.models.product import Product
from app.schemas.cart_item_schema import cart_item_schema, cart_items_schema
from app.extensions import db

cart_bp = Blueprint("cart_bp", __name__, url_prefix="/cart")

@cart_bp.route("/", methods=["GET"])
def get_cart_items():
    """
    Retrieves all items in the cart.
    """
    # For now, we fetch all cart items. In a real app, you'd filter by the current user's ID.
    cart_items = CartItem.query.all()
    
    # Serialize the cart items to include product details
    result = cart_items_schema.dump(cart_items)
    
    return jsonify(result), 200

@cart_bp.route("/add", methods=["POST"])
def add_to_cart():
    """
    Adds a product to the cart or updates its quantity if it already exists.
    """
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # For now, we'll get the first user or create one if none exist.
    # In a real app, you would get the user from the session or a token.
    user = User.query.first()
    if not user:
        user = User(
            name="Default User",
            email="default@example.com",
            password_hash="default_password",  # In a real app, hash this properly
        )
        db.session.add(user)
        db.session.commit()

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product.id).first()

    if cart_item:
        # If item exists, update quantity
        cart_item.quantity += int(quantity)
    else:
        # If item doesn't exist, create a new one
        cart_item = CartItem(
            user_id=user.id,
            product_id=product.id,
            quantity=int(quantity)
        )
        db.session.add(cart_item)

    db.session.commit()

    # Serialize the cart item to include product details
    result = cart_item_schema.dump(cart_item)

    return jsonify(result), 201

@cart_bp.route("/item/<int:item_id>", methods=["PATCH"])
def update_cart_item(item_id):
    """
    Updates the quantity of a specific cart item.
    """
    data = request.get_json()
    quantity = data.get("quantity")

    if quantity is None:
        return jsonify({"error": "Quantity is required"}), 400

    cart_item = CartItem.query.get(item_id)

    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    quantity = int(quantity)
    if quantity <= 0:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Item removed from cart"}), 200
    else:
        cart_item.quantity = quantity
        db.session.commit()
        result = cart_item_schema.dump(cart_item)
        return jsonify(result), 200

@cart_bp.route("/item/<int:item_id>", methods=["DELETE"])
def delete_cart_item(item_id):
    """
    Deletes a specific cart item.
    """
    cart_item = CartItem.query.get(item_id)

    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Item removed from cart"}), 200
