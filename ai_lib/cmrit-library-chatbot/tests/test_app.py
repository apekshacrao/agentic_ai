import unittest

from app import app
from chatbot import chatbot_response


class ChatbotTests(unittest.TestCase):
    def test_book_search_returns_rack(self):
        response = chatbot_response("Where can I find DBMS?")
        self.assertIn("Rack: B-07", response)

    def test_unknown_message_has_help(self):
        response = chatbot_response("Tell me something unrelated")
        self.assertIn("Try asking", response)


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_empty_message_is_rejected(self):
        response = self.client.post("/chat", json={"message": " "})
        self.assertEqual(response.status_code, 400)

    def test_valid_message_is_answered(self):
        response = self.client.post("/chat", json={"message": "library timings"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Monday-Friday", response.json["response"])


if __name__ == "__main__":
    unittest.main()
