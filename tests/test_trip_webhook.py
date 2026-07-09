"""Тесты webhook-уведомлений."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from services.trip_webhook import notify_completion, sign_payload


class TestTripWebhook(unittest.TestCase):
    def test_sign_payload_deterministic(self) -> None:
        body = '{"trip_id": 1, "status": "completed"}'
        self.assertEqual(sign_payload(1, body), sign_payload(1, body))

    @patch("services.trip_webhook.requests.post")
    def test_notify_posts_json(self, mock_post: MagicMock) -> None:
        mock_post.return_value = MagicMock(status_code=200, raise_for_status=MagicMock())
        code = notify_completion(
            callback_url="https://example.com/hook",
            trip_id=7,
            status="completed",
        )
        self.assertEqual(code, 200)
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
