from flask import Blueprint, request, jsonify
from ..models import User
from .. import db
from ..services.user_service import create_user_service
from ..services.user_service import (
    create_user_service,
    update_user_service,
    delete_user_service,
    get_all_users_service,
    get_user_service
)
users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_all_users():
    return get_all_users_service()


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return get_user_service(user_id)


@users_bp.route("/", methods=["POST"])
def create_user():
    return create_user_service(request)


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    return update_user_service(user_id, request)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    return delete_user_service(user_id)
