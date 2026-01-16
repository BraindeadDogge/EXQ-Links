import os

from flask import Blueprint, Flask, jsonify, redirect, request

from ..db import session_scope
from ..services.shortener import dump_store, get_or_create_short_id, resolve_short_id


def register_shortener_routes(app: Flask) -> None:
  bp = Blueprint("shortener", __name__)

  @bp.get("/shorten")
  def shorten():
    original_url = (request.args.get("url") or "").strip()
    if not original_url:
      return jsonify({"error": "Missing required 'url' query parameter"}), 400

    with session_scope() as session:
      short_id = get_or_create_short_id(session, original_url)
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.headers.get("X-Forwarded-Host", request.host)
    actual_host = os.getenv("SHORT_HOST", host)

    short_link = f"{proto}://{actual_host}/{short_id}"
    return jsonify(
      {
        "original_url": original_url,
        "short_id": short_id,
        "short_url": short_link,
      }
    ), 201

  @bp.get("/debug/log-stores")
  def log_stores():
    with session_scope() as session:
      return jsonify({"rows": dump_store(session)}), 200

  @bp.get("/<short_id>")
  def resolve_short(short_id: str):
    with session_scope() as session:
      target = resolve_short_id(session, short_id)
    if not target:
      return jsonify({"error": "Unknown short link"}), 404
    return redirect(target)

  app.register_blueprint(bp)
