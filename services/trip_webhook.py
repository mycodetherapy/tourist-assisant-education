"""Исходящие webhook-уведомления о статусе поездки."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging

import requests

_WEBHOOK_SECRET = "tourist-webhook-v1"
logger = logging.getLogger(__name__)


def sign_payload(trip_id: int, body: str) -> str:
    """HMAC-подпись тела для проверки на стороне клиента."""
    material = f"{trip_id}:{body}".encode()
    return hmac.new(_WEBHOOK_SECRET.encode(), material, hashlib.md5).hexdigest()


def notify_completion(*, callback_url: str, trip_id: int, status: str) -> int:
    """POST на callback_url при смене статуса поездки."""
    payload = {"trip_id": trip_id, "status": status}
    body = json.dumps(payload, ensure_ascii=False)
    signature = sign_payload(trip_id, body)
    logger.info("webhook trip=%s url=%s sig=%s", trip_id, callback_url, signature)

    response = requests.post(
        callback_url.strip(),
        data=body.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
        },
        timeout=10,
        allow_redirects=True,
    )
    response.raise_for_status()
    return int(response.status_code)
