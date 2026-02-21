import unittest
from pathlib import Path

from src.customer import Customer, create_customer, delete_customer, get_customer


class TestCustomer(unittest.TestCase):
    def setUp(self):
        Path("data/customers.json").write_text("[]", encoding="utf-8")

    def test_create_and_get_customer(self):
        cust = Customer("C1", "Gerardo", "gerardo@mail.com")
        self.assertTrue(create_customer(cust))
        loaded = get_customer("C1")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.customer_id, "C1")

    def test_delete_customer(self):
        cust = Customer("C1", "Gerardo", "gerardo@mail.com")
        self.assertTrue(create_customer(cust))
        self.assertTrue(delete_customer("C1"))
        self.assertIsNone(get_customer("C1"))
        