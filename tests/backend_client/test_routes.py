import os
import time
from urllib.parse import urlencode

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def wait_for_ping(base_url: str, timeout: float = 180.0, interval: float = 0.5) -> None:
  """Poll /ping until it responds with the expected payload"""
  deadline = time.time() + timeout
  url = f"{base_url.rstrip('/')}/ping"
  while time.time() < deadline:
    try:
      response = requests.get(url, timeout=2)
      if response.status_code == 200:
        payload = response.json()
        if payload.get("status") == "ok" and payload.get("data") == "pong":
          return
    except requests.RequestException:
      pass
    time.sleep(interval)
  raise TimeoutError(f"Timed out waiting for {url}")


@pytest.fixture(scope="session", autouse=True)
def wait_for_service() -> None:
  wait_for_ping(BASE_URL)


def test_shorten() -> None:
  """Create a short link and verify it redirects to the original URL"""
  base = BASE_URL.rstrip("/")
  target_url = "https://example.com/docs"
  shorten_url = f"{base}/shorten?{urlencode({'url': target_url})}"
  response = requests.get(shorten_url, timeout=5)
  response.raise_for_status()
  payload = response.json()

  short_id = payload.get("short_id")
  short_url = payload.get("short_url")
  assert short_id
  assert short_url
  assert short_url.endswith(f"/{short_id}")

  redirect_response = requests.get(short_url, timeout=5, allow_redirects=False)
  assert redirect_response.status_code == 302
  assert redirect_response.headers.get("Location") == target_url


def test_newsletter() -> None:
  """Subscribe an email and ensure idempotent behavior"""
  base = BASE_URL.rstrip("/")
  email = f"tester+{int(time.time())}@example.com"
  subscribe_url = f"{base}/newsletter/subscribe"

  response = requests.post(subscribe_url, json={"email": email}, timeout=5)
  response.raise_for_status()
  payload = response.json()

  assert payload.get("email") == email
  assert payload.get("subscribed") is True
  assert payload.get("is_new") is True

  # Second attempt should be idempotent (200) and not blow up.
  second = requests.post(subscribe_url, json={"email": email}, timeout=5)
  assert second.status_code == 200
  second_payload = second.json()
  assert second_payload.get("is_new") is False
