from copy import deepcopy
from typing import Any, Dict


OPENAPI_SPEC: Dict[str, Any] = {
  "openapi": "3.0.3",
  "info": {
    "title": "Link Shortener API",
    "version": "1.0.0",
    "description": "API for shortening URLs and managing newsletter subscriptions.",
  },
  "paths": {
    "/ping": {
      "get": {
        "summary": "Health check",
        "responses": {
          "200": {
            "description": "Service is healthy",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/PingResponse"}
              }
            },
          }
        },
      }
    },
    "/shorten": {
      "get": {
        "summary": "Shorten a URL",
        "parameters": [
          {
            "name": "url",
            "in": "query",
            "required": True,
            "schema": {"type": "string", "format": "uri"},
          }
        ],
        "responses": {
          "201": {
            "description": "Short URL created or reused",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/ShortenResponse"}
              }
            },
          },
          "400": {
            "description": "Missing or invalid URL",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/Error"}
              }
            },
          },
        },
      }
    },
    "/debug/log-stores": {
      "get": {
        "summary": "List recent short URL mappings",
        "responses": {
          "200": {
            "description": "Recent stored URLs",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/DebugLogStoresResponse"}
              }
            },
          }
        },
      }
    },
    "/{short_id}": {
      "get": {
        "summary": "Resolve a short ID",
        "parameters": [
          {
            "name": "short_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
          }
        ],
        "responses": {
          "302": {
            "description": "Redirect to the original URL",
            "headers": {
              "Location": {"schema": {"type": "string", "format": "uri"}}
            },
          },
          "404": {
            "description": "Unknown short link",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/Error"}
              }
            },
          },
        },
      }
    },
    "/newsletter/subscribe": {
      "post": {
        "summary": "Subscribe to the newsletter",
        "requestBody": {
          "required": True,
          "content": {
            "application/json": {
              "schema": {"$ref": "#/components/schemas/NewsletterSubscribeRequest"}
            }
          },
        },
        "responses": {
          "200": {
            "description": "Email already subscribed",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/NewsletterSubscribeResponse"
                }
              }
            },
          },
          "201": {
            "description": "Email subscribed",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/NewsletterSubscribeResponse"
                }
              }
            },
          },
          "400": {
            "description": "Invalid email",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/Error"}
              }
            },
          },
        },
      }
    },
    "/newsletter/base": {
      "get": {
        "summary": "List recent newsletter subscribers",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "minimum": 1, "default": 50},
          }
        ],
        "responses": {
          "200": {
            "description": "Recent subscribers",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/NewsletterBaseResponse"}
              }
            },
          },
          "400": {
            "description": "Invalid limit",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/Error"}
              }
            },
          },
        },
      }
    },
  },
  "components": {
    "schemas": {
      "PingResponse": {
        "type": "object",
        "properties": {
          "status": {"type": "string"},
          "data": {"type": "string"},
        },
        "required": ["status", "data"],
      },
      "Error": {
        "type": "object",
        "properties": {"error": {"type": "string"}},
        "required": ["error"],
      },
      "ShortenResponse": {
        "type": "object",
        "properties": {
          "original_url": {"type": "string", "format": "uri"},
          "short_id": {"type": "string"},
          "short_url": {"type": "string", "format": "uri"},
        },
        "required": ["original_url", "short_id", "short_url"],
      },
      "ShortURLRow": {
        "type": "object",
        "properties": {
          "short_id": {"type": "string"},
          "original_url": {"type": "string", "format": "uri"},
          "created_at": {"type": "string", "format": "date-time"},
        },
        "required": ["short_id", "original_url", "created_at"],
      },
      "DebugLogStoresResponse": {
        "type": "object",
        "properties": {
          "rows": {
            "type": "array",
            "items": {"$ref": "#/components/schemas/ShortURLRow"},
          }
        },
        "required": ["rows"],
      },
      "NewsletterSubscribeRequest": {
        "type": "object",
        "properties": {"email": {"type": "string", "format": "email"}},
        "required": ["email"],
      },
      "NewsletterSubscribeResponse": {
        "type": "object",
        "properties": {
          "email": {"type": "string", "format": "email"},
          "subscribed": {"type": "boolean"},
          "is_new": {"type": "boolean"},
          "message": {"type": "string"},
        },
        "required": ["email", "subscribed", "is_new"],
      },
      "Subscriber": {
        "type": "object",
        "properties": {
          "email": {"type": "string", "format": "email"},
          "created_at": {"type": "string", "format": "date-time"},
        },
        "required": ["email", "created_at"],
      },
      "NewsletterBaseResponse": {
        "type": "object",
        "properties": {
          "rows": {
            "type": "array",
            "items": {"$ref": "#/components/schemas/Subscriber"},
          }
        },
        "required": ["rows"],
      },
    }
  },
}


def get_openapi_spec(base_url: str) -> Dict[str, Any]:
  spec = deepcopy(OPENAPI_SPEC)
  if base_url:
    spec["servers"] = [{"url": base_url}]
  return spec
