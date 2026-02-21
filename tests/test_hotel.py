import unittest
from pathlib import Path

from src.hotel import Hotel, create_hotel, delete_hotel, get_hotel


class TestHotel(unittest.TestCase):
    def setUp(self):
        Path("data/hotels.json").write_text("[]", encoding="utf-8")

    def test_create_and_get_hotel(self):
        hotel = Hotel("H1", "Hotel Centro", "MTY", 10, 10)
        ok = create_hotel(hotel)
        self.assertTrue(ok)

        loaded = get_hotel("H1")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.hotel_id, "H1")

    def test_delete_hotel(self):
        hotel = Hotel("H1", "Hotel Centro", "MTY", 10, 10)
        self.assertTrue(create_hotel(hotel))
        self.assertTrue(delete_hotel("H1"))
        self.assertIsNone(get_hotel("H1"))
