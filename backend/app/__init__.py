import os

from flask import Flask, jsonify
from flask_cors import CORS

from .db import init_engine
from .routes.newsletter import register_newsletter_routes
from .routes.shortener import register_shortener_routes


def create_app():
  app = Flask(__name__)
  allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
  ]
  CORS(app, origins=allowed_origins)
  init_engine()

  @app.get("/ping")
  def ping():
    return jsonify({"status": "ok", "data": "pong"}), 200

  register_shortener_routes(app)
  register_newsletter_routes(app)

  return app


if __name__ == "__main__":
  port = int(os.getenv("PORT", "8000"))
  create_app().run(host="0.0.0.0", port=port)
