from flask import Blueprint, jsonify
from app.models import db, User, Product, CartItem, AffiliateSource
from app.schemas import ProductSchema, CartItemSchema

main_routes = Blueprint("main_routes", __name__)

# Schemas
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

# --- ShipmentSummary ---
@main_routes.route("/shipments/summary", methods=["GET"])
def shipment_summary():
    # Example: total cart items and users
    total_items = CartItem.query.count()
    total_users = User.query.count()
    return jsonify({"total_items": total_items, "total_users": total_users})

# --- TopProducts ---
@main_routes.route("/products/top", methods=["GET"])
def top_products():
    # Example: top 5 products by number of times added to cart
    products = (
        db.session.query(Product, db.func.count(CartItem.id).label("cart_count"))
        .join(CartItem, Product.id == CartItem.product_id)
        .group_by(Product.id)
        .order_by(db.desc("cart_count"))
        .limit(5)
        .all()
    )
    result = [
        {"id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url, "cart_count": count}
        for p, count in products
    ]
    return jsonify(result)

# --- ItemsShipped ---
@main_routes.route("/shipments/items", methods=["GET"])
def items_shipped():
    # Example: total quantity of items shipped
    total_quantity = db.session.query(db.func.sum(CartItem.quantity)).scalar() or 0
    return jsonify({"total_quantity": total_quantity})

# --- LevelComparison ---
@main_routes.route("/metrics/level", methods=["GET"])
def level_comparison():
    # Example: compare number of items added this month vs last month
    from datetime import datetime, timedelta
    from sqlalchemy import extract

    now = datetime.utcnow()
    last_month = now.replace(day=1) - timedelta(days=1)
    
    this_month_count = CartItem.query.filter(extract('month', CartItem.added_at) == now.month).count()
    last_month_count = CartItem.query.filter(extract('month', CartItem.added_at) == last_month.month).count()

    return jsonify({"this_month": this_month_count, "last_month": last_month_count})

# --- DonutChart ---
@main_routes.route("/charts/donut", methods=["GET"])
def donut_chart():
    # Example: percentage of products per affiliate source
    results = (
        db.session.query(AffiliateSource.name, db.func.count(Product.id))
        .join(Product)
        .group_by(AffiliateSource.id)
        .all()
    )
    chart_data = [{"affiliate": name, "count": count} for name, count in results]
    return jsonify(chart_data)

# --- SalesGraph ---
@main_routes.route("/charts/sales", methods=["GET"])
def sales_graph():
    # Example: total quantity per day for last 7 days
    from datetime import datetime, timedelta
    results = []
    for i in range(7):
        day = datetime.utcnow() - timedelta(days=i)
        count = CartItem.query.filter(
            db.func.date(CartItem.added_at) == day.date()
        ).count()
        results.append({"date": day.strftime("%Y-%m-%d"), "count": count})
    return jsonify(list(reversed(results)))
