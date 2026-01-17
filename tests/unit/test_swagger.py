import os
import sys

import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
  sys.path.insert(0, BACKEND_DIR)

from app import create_app


@pytest.fixture()
def client(monkeypatch):
  monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
  monkeypatch.setenv("DB_CONNECT_RETRIES", "0")
  monkeypatch.setenv("DB_CONNECT_RETRY_INTERVAL", "0")
  app = create_app()
  app.testing = True
  return app.test_client()


def test_ping(client):
  response = client.get("/ping")
  assert response.status_code == 200
  payload = response.get_json()
  assert payload.get("status") == "ok"
  assert payload.get("data") == "pong"


def test_swagger_json(client):
  response = client.get("/swagger.json", base_url="http://localhost:8000")
  assert response.status_code == 200
  payload = response.get_json()
  assert payload.get("openapi") == "3.0.3"
  assert "/newsletter/subscribe" in payload.get("paths", {})
  servers = payload.get("servers", [])
  assert servers
  assert servers[0].get("url") == "http://localhost:8000"
