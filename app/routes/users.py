from flask import Blueprint, request, jsonify
from app.models import db, User
from app.schemas import UserSchema

user_bp = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# GET all users
@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200

# GET single user
@user_bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user), 200

# POST new user
@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

# PATCH user
@user_bp.route("/<int:id>", methods=["PATCH"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.jsonify(user), 200

# DELETE user
@user_bp.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
