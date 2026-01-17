import atexit
import os
import time

from flask import Flask, g, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .db import init_engine
from .routes.auth import register_auth_routes
from .routes.newsletter import register_newsletter_routes
from .routes.shortener import register_shortener_routes


def create_app():
  app = Flask(__name__)
  allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
  ]
  app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
  app.config["SESSION_COOKIE_HTTPONLY"] = True
  app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
  app.config["SESSION_COOKIE_SECURE"] = os.getenv(
      "SESSION_COOKIE_SECURE", "false"
  ).lower() == "true"
  session_domain = os.getenv("SESSION_COOKIE_DOMAIN")
  if session_domain:
    app.config["SESSION_COOKIE_DOMAIN"] = session_domain

  CORS(app, origins=allowed_origins, supports_credentials=True)
  app.logger.info("App startup")
  init_engine(logger=app.logger)

  @app.before_request
  def log_request_start():
    g.request_start = time.perf_counter()
    app.logger.info("Request start: %s %s", request.method, request.path)

  @app.after_request
  def log_request_end(response):
    start = getattr(g, "request_start", None)
    if start is not None:
      duration_ms = (time.perf_counter() - start) * 1000
      app.logger.info(
          "Request end: %s %s %s %.2fms",
          request.method,
          request.path,
          response.status_code,
          duration_ms,
      )
    else:
      app.logger.info(
          "Request end: %s %s %s",
          request.method,
          request.path,
          response.status_code,
      )
    return response

  @app.teardown_request
  def log_request_exception(exc):
    if exc is not None:
      if isinstance(exc, HTTPException) and (exc.code or 0) < 500:
        app.logger.warning(
            "Client error during request: %s %s %s",
            request.method,
            request.path,
            exc.code,
        )
      else:
        app.logger.error(
            "Unhandled exception during request: %s %s",
            request.method,
            request.path,
            exc_info=exc,
        )

  def _log_shutdown() -> None:
    app.logger.info("App shutdown")

  atexit.register(_log_shutdown)

  @app.get("/ping")
  def ping():
    return jsonify({"status": "ok", "data": "pong"}), 200

  def _is_dev_mode() -> bool:
    env = os.getenv("FLASK_ENV", "").lower()
    if env == "development":
      return True
    debug_env = os.getenv("FLASK_DEBUG", "").lower()
    return debug_env in ("1", "true", "yes")

  if _is_dev_mode():
    try:
      from flask_swagger_ui import get_swaggerui_blueprint
    except Exception as exc:
      app.logger.warning("Swagger UI unavailable: %s", exc)
      get_swaggerui_blueprint = None

    from .openapi import get_openapi_spec

    if get_swaggerui_blueprint is not None:
      swagger_url = "/docs"
      swagger_api_url = "/swagger.json"
      swaggerui_blueprint = get_swaggerui_blueprint(
          swagger_url,
          swagger_api_url,
          config={"app_name": "Link Shortener API"},
      )
      app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    @app.get("/swagger.json")
    def swagger_spec():
      base_url = request.host_url.rstrip("/")
      return jsonify(get_openapi_spec(base_url)), 200

  register_shortener_routes(app)
  register_auth_routes(app)
  register_newsletter_routes(app)

  return app


if __name__ == "__main__":
  port = int(os.getenv("PORT", "8000"))
  create_app().run(host="0.0.0.0", port=port)
