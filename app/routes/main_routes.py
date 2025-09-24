from flask import Blueprint, jsonify
from app.models import db, User, Product, CartItem, AffiliateSource
from app.schemas import ProductSchema, CartItemSchema
from datetime import datetime, timedelta
from sqlalchemy import extract, func

main_routes = Blueprint("main_routes", __name__)

# Schemas
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

# --- Shipment Summary ---
@main_routes.route("/shipments/summary", methods=["GET"])
def shipment_summary():
    """Returns total cart items and total users."""
    total_items = CartItem.query.count()
    total_users = User.query.count()
    return jsonify({"total_items": total_items, "total_users": total_users})


# --- Top Products ---
@main_routes.route("/products/top", methods=["GET"])
def top_products():
    """Returns top 5 products by number of times added to cart."""
    products = (
        db.session.query(Product, func.count(CartItem.id).label("cart_count"))
        .join(CartItem, Product.id == CartItem.product_id)
        .group_by(Product.id)
        .order_by(db.desc("cart_count"))
        .limit(5)
        .all()
    )
    result = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price) if p.price else None,  # ensure JSON serializable
            "image_url": p.image_url,
            "cart_count": count,
        }
        for p, count in products
    ]
    return jsonify(result)


# --- Items Shipped ---
@main_routes.route("/shipments/items", methods=["GET"])
def items_shipped():
    """Returns total quantity of items shipped (cart quantities)."""
    total_quantity = db.session.query(func.sum(CartItem.quantity)).scalar() or 0
    return jsonify({"total_quantity": total_quantity})


# --- Level Comparison ---
@main_routes.route("/metrics/level", methods=["GET"])
def level_comparison():
    """Compares number of items added this month vs last month."""
    now = datetime.utcnow()
    last_month = now.replace(day=1) - timedelta(days=1)

    this_month_count = CartItem.query.filter(
        extract("month", CartItem.added_at) == now.month
    ).count()

    last_month_count = CartItem.query.filter(
        extract("month", CartItem.added_at) == last_month.month
    ).count()

    return jsonify({"this_month": this_month_count, "last_month": last_month_count})


# --- Donut Chart ---
@main_routes.route("/charts/donut", methods=["GET"])
def donut_chart():
    """Returns percentage of products per affiliate source."""
    results = (
        db.session.query(AffiliateSource.name, func.count(Product.id))
        .join(Product)
        .group_by(AffiliateSource.id)
        .all()
    )
    chart_data = [{"affiliate": name, "count": count} for name, count in results]
    return jsonify(chart_data)


# --- Sales Graph ---
@main_routes.route("/charts/sales", methods=["GET"])
def sales_graph():
    """Returns total quantity per day for the last 7 days."""
    results = []
    for i in range(7):
        day = datetime.utcnow() - timedelta(days=i)
        count = CartItem.query.filter(
            func.date(CartItem.added_at) == day.date()
        ).count()
        results.append({"date": day.strftime("%Y-%m-%d"), "count": count})
    return jsonify(list(reversed(results)))
