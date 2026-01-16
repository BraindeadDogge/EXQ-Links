import re

from flask import Blueprint, Flask, jsonify, request

from ..db import session_scope
from ..services.newsletter import get_recent_subscribers, subscribe_email

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _is_valid_email(address: str) -> bool:
  return bool(EMAIL_PATTERN.match(address))


def register_newsletter_routes(app: Flask) -> None:
  bp = Blueprint("newsletter", __name__, url_prefix="/newsletter")

  @bp.post("/subscribe")
  def subscribe():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
      payload = {}

    raw_email = payload.get("email") or ""
    email = raw_email.strip().lower()

    if not email:
      return jsonify({"error": "Email is required"}), 400
    if not _is_valid_email(email):
      return jsonify({"error": "Invalid email address"}), 400

    with session_scope() as session:
      created = subscribe_email(session, email)
    status_code = 201 if created else 200
    message = "Subscribed" if created else "Already subscribed"

    return (
      jsonify(
        {
          "email": email,
          "subscribed": True,
          "is_new": created,
          "message": message,
        }
      ),
      status_code,
    )

  @bp.get("/base")
  def list_base():
    raw_limit = request.args.get("limit")
    limit = 50
    if raw_limit is not None:
      try:
        limit = int(raw_limit)
      except ValueError:
        return jsonify({"error": "Invalid limit"}), 400
      if limit <= 0:
        return jsonify({"error": "Limit must be positive"}), 400

    with session_scope() as session:
      rows = get_recent_subscribers(session, limit=limit)
    return jsonify({"rows": rows}), 200

  app.register_blueprint(bp)
