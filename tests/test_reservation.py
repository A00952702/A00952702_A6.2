import unittest
from pathlib import Path

from src.customer import Customer, create_customer
from src.hotel import Hotel, create_hotel, get_hotel
from src.reservation import Reservation, cancel_reservation, create_reservation


class TestReservation(unittest.TestCase):
    def setUp(self):
        Path("data/hotels.json").write_text("[]", encoding="utf-8")
        Path("data/customers.json").write_text("[]", encoding="utf-8")
        Path("data/reservations.json").write_text("[]", encoding="utf-8")

        self.assertTrue(create_hotel(Hotel("H1", "Hotel Centro", "MTY", 2, 2)))
        self.assertTrue(create_customer(Customer("C1", "Gerardo", "g@mail.com")))

    def test_create_reservation_decreases_rooms(self):
        ok = create_reservation(Reservation("R1", "H1", "C1"))
        self.assertTrue(ok)

        hotel = get_hotel("H1")
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.available_rooms, 1)

    def test_cancel_reservation_increases_rooms(self):
        self.assertTrue(create_reservation(Reservation("R1", "H1", "C1")))
        self.assertTrue(cancel_reservation("R1"))

        hotel = get_hotel("H1")
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.available_rooms, 2)