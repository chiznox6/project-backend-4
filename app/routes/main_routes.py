from flask import Blueprint, jsonify, request
from app.models import db, User, Product, CartItem, AffiliateSource
from app.schemas import ProductSchema, CartItemSchema
from datetime import datetime, timedelta
from sqlalchemy import extract, func
from decimal import Decimal

# Import Amazon service functions
from app.services.amazon_service import (
    search_amazon_products,
    get_product_details,
    get_product_reviews,
)

main_routes = Blueprint("main_routes", __name__)

# Schemas
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)


# ===============================
# 🚚 Shipment + Analytics Routes
# ===============================

@main_routes.route("/shipments/summary", methods=["GET"])
def shipment_summary():
    """Returns total cart items and total users."""
    total_items = CartItem.query.count()
    total_users = User.query.count()
    return jsonify({"total_items": total_items, "total_users": total_users})



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
            "price": float(p.price) if p.price else None,
            "image_url": p.image_url,
            "cart_count": count,
        }
        for p, count in products
    ]
    return jsonify(result)



@main_routes.route("/shipments/items", methods=["GET"])
def items_shipped():
    """Returns total quantity of items shipped (cart quantities)."""
    total_quantity = db.session.query(func.sum(CartItem.quantity)).scalar() or 0
    return jsonify({"total_quantity": total_quantity})



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


# ===============================
# 🛒 Amazon API Routes
# ===============================

@main_routes.route("/amazon/search", methods=["GET"])
def amazon_search():
    """Search Amazon products live from API."""
    query = request.args.get("query")
    page = request.args.get("page", 1, type=int)
    country = request.args.get("country", "US")
    sort_by = request.args.get("sort_by", "RELEVANCE")

    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400

    data = search_amazon_products(query, page, country, sort_by)
    return jsonify(data)


@main_routes.route("/amazon/product/<asin>", methods=["GET"])
def amazon_product_details(asin):
    """Fetch Amazon product details by ASIN."""
    country = request.args.get("country", "US")
    data = get_product_details(asin, country)
    return jsonify(data)


@main_routes.route("/amazon/product/<asin>/reviews", methods=["GET"])
def amazon_product_reviews(asin):
    """Fetch Amazon product reviews by ASIN."""
    country = request.args.get("country", "US")
    page = request.args.get("page", 1, type=int)
    sort_by = request.args.get("sort_by", "TOP_REVIEWS")

    data = get_product_reviews(asin, country, page, sort_by)
    return jsonify(data)

@main_routes.route("/seed", methods=["GET"])
def seed_database():
    """Seeds the database with initial data."""
    # Create an affiliate source if it doesn't exist
    amazon_source = AffiliateSource.query.filter_by(name="Amazon").first()
    if not amazon_source:
        amazon_source = AffiliateSource(name="Amazon", api_name="amazon", base_url="https://www.amazon.com")
        db.session.add(amazon_source)
        db.session.commit()

    # Create some products
    products_to_create = [
        {
            "name": "Wireless Mouse",
            "price": Decimal("25.99"),
            "image_url": "https://via.placeholder.com/150",
            "affiliate_link": "https://www.amazon.com/dp/B07S395R4P",
            "affiliate_source_id": amazon_source.id,
        },
        {
            "name": "Mechanical Keyboard",
            "price": Decimal("79.99"),
            "image_url": "https://via.placeholder.com/150",
            "affiliate_link": "https://www.amazon.com/dp/B07S395R4P",
            "affiliate_source_id": amazon_source.id,
        },
        {
            "name": "USB-C Hub",
            "price": Decimal("39.99"),
            "image_url": "https://via.placeholder.com/150",
            "affiliate_link": "https://www.amazon.com/dp/B07S395R4P",
            "affiliate_source_id": amazon_source.id,
        },
    ]

    for product_data in products_to_create:
        product = Product.query.filter_by(name=product_data["name"]).first()
        if not product:
            new_product = Product(**product_data)
            db.session.add(new_product)

    db.session.commit()

    return jsonify({"message": "Database seeded successfully!"}), 200
