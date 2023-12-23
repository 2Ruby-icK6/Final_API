import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<form action=\"/login\" method=\"POST\">", response.data.decode())
        self.assertIn("<label for=\"\">Username:</label>", response.data.decode())
        self.assertIn("<label for=\"\">Password:</label>", response.data.decode())

    def test_login_success(self):
        response = self.app.post("/login", data={"username": "your_username", "password": "12345678"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data.decode())

    def test_login_failure(self):
        response = self.app.post("/login", data={"username": "invalid_username", "password": "invalid_password"})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Unable to verify", response.data.decode())

    def test_get_clients(self):
        response = self.app.get("/client")
        self.assertEqual(response.status_code, 200)

    def test_add_client(self):
        data = {
            "client_name": "New Client",
            "work_date": "2023-01-01",
            "avg_datebillings": '2015-05-29 12:22:36',
            "projectcount_kpi": 5,
        }
        response = self.app.post("/client", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Added Successfully", response.data.decode())

    def test_update_client(self):
        data = {
            "client_name": "Updated Client",
            "work_date": "2023-02-01",
            "avg_datebillings": '2005-05-29 12:22:36',
            "projectcount_kpi": 7,
        }
        response = self.app.put("/client/1", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Successfully", response.data.decode())

    def test_delete_client(self):
        response = self.app.delete("/client/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Deleted Successfully", response.data.decode())


if __name__ == "__main__":
    unittest.main()
