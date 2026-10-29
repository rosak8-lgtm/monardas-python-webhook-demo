import unittest
from webhook_demo import process, seen

class WebhookDemoTests(unittest.TestCase):
    def setUp(self):
        seen.clear()

    def test_accepts_valid(self):
        status, body = process({"lead_id": "001", "email": "TEST@EXAMPLE.COM"})
        self.assertEqual(status, 201)
        self.assertEqual(body["email"], "test@example.com")

    def test_duplicate_safe(self):
        process({"lead_id": "001", "email": "a@example.com"})
        status, body = process({"lead_id": "001", "email": "a@example.com"})
        self.assertEqual((status, body["status"]), (200, "duplicate"))

    def test_invalid_email(self):
        self.assertEqual(process({"lead_id": "01", "email": "invalid"})[0], 422)

    def test_invalid_id(self):
        self.assertEqual(process({"lead_id": "bad id", "email": "a@example.com"})[0], 422)

    def test_invalid_payload(self):
        self.assertEqual(process([])[0], 400)

if __name__ == "__main__":
    unittest.main()
