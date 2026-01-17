import re
from typing import Any, Dict

from flask import Blueprint, Flask, jsonify, request, session

from ..db import session_scope
from ..services.auth import authenticate_user, create_user, get_user_by_id

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _is_valid_email(address: str) -> bool:
  return bool(EMAIL_PATTERN.match(address))


def _serialize_user(user) -> Dict[str, Any]:
  return {
    "id": user.id,
    "email": user.email,
    "created_at": user.created_at.isoformat(),
    "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
  }


def register_auth_routes(app: Flask) -> None:
  bp = Blueprint("auth", __name__, url_prefix="/auth")

  @bp.post("/register")
  def register():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
      payload = {}

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email:
      return jsonify({"error": "Email is required"}), 400
    if not _is_valid_email(email):
      return jsonify({"error": "Invalid email address"}), 400
    if len(password) < 8:
      return jsonify({"error": "Password must be at least 8 characters"}), 400

    with session_scope() as session_db:
      user = create_user(session_db, email, password)
      if not user:
        return jsonify({"error": "Email already registered"}), 409
      session["user_id"] = user.id
      app.logger.info("User registered: %s", user.email)
      return jsonify({"user": _serialize_user(user)}), 201

  @bp.post("/login")
  def login():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
      payload = {}

    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    remember = bool(payload.get("remember"))

    if not email or not password:
      return jsonify({"error": "Email and password are required"}), 400

    with session_scope() as session_db:
      user = authenticate_user(session_db, email, password)
      if not user:
        return jsonify({"error": "Invalid credentials"}), 401
      session["user_id"] = user.id
      session.permanent = remember
      app.logger.info("User logged in: %s", user.email)
      return jsonify({"user": _serialize_user(user)}), 200

  @bp.post("/logout")
  def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

  @bp.get("/me")
  def me():
    user_id = session.get("user_id")
    if not user_id:
      return jsonify({"error": "Unauthorized"}), 401

    with session_scope() as session_db:
      user = get_user_by_id(session_db, user_id)
      if not user:
        session.clear()
        return jsonify({"error": "Unauthorized"}), 401
      return jsonify({"user": _serialize_user(user)}), 200

  app.register_blueprint(bp)
