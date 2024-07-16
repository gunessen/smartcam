from flask import Blueprint, jsonify, request

from services import user_service

login_bp = Blueprint("login", __name__)


@login_bp.route("/api/v1/login", methods=["POST"])
def get_token():
    try:
        data = request.get_json()

        if user_service.authenticate_user(data["username"], data["password"]):
            return jsonify({"token": "1234"}, 200)
        else:
            return jsonify({"error": "Invalid username or password"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400
