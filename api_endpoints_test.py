import unittest
from app import app

class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
    