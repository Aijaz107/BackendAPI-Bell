from flask import jsonify
from werkzeug.utils import secure_filename
from ..models import User
from .. import db
import os

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_all_users_service():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'image': user.image  # Only send the filename, not the full path
        })
    return jsonify(users_list), 200


def get_user_service(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200

def create_user_service(request):
    data = request.form

    required_fields = ["first_name", "last_name", "email", "password"]
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    image_file = request.files.get("image")

    filename = None
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join("uploads/photos", filename)
        image_file.save(upload_path)

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data["password"],  # In real app: hash this
        image=filename
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

def update_user_service(user_id, request):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.form

    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)

    # Handle image update
    image_file = request.files.get("image")
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join("uploads/photos", filename)
        image_file.save(upload_path)
        user.image = filename

    db.session.commit()

    return jsonify(user.to_dict()), 200

def delete_user_service(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Delete image file if exists
    if user.image:
        image_path = os.path.join("uploads/photos", user.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

