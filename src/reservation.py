"""
reservation.py
Reservation entity + persistence operations.
Creating a reservation decreases hotel available rooms.
Canceling a reservation increases hotel available rooms.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from src.customer import get_customer
from src.hotel import (
    cancel_reservation_room,
    get_hotel,
    reserve_room,
)
from src.storage import read_json_list, write_json_list

RESERVATIONS_FILE = "data/reservations.json"


@dataclass
class Reservation:
    """Represents a reservation."""
    reservation_id: str
    hotel_id: str
    customer_id: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON persistence."""
        return {
            "reservation_id": self.reservation_id,
            "hotel_id": self.hotel_id,
            "customer_id": self.customer_id,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Reservation":
        """Create a Reservation from a dict."""
        return Reservation(
            reservation_id=str(data["reservation_id"]),
            hotel_id=str(data["hotel_id"]),
            customer_id=str(data["customer_id"]),
        )


def _load_all() -> list[Reservation]:
    items = read_json_list(RESERVATIONS_FILE)
    return [Reservation.from_dict(x) for x in items]


def _save_all(reservations: list[Reservation]) -> None:
    write_json_list(RESERVATIONS_FILE, [r.to_dict() for r in reservations])


def get_reservation(reservation_id: str) -> Optional[Reservation]:
    """Get reservation by ID."""
    reservations = _load_all()
    for r in reservations:
        if r.reservation_id == reservation_id:
            return r
    return None


def create_reservation(reservation: Reservation) -> bool:
    """
    Create reservation:
    - reservation_id must be unique
    - hotel must exist
    - customer must exist
    - reserve_room(hotel_id) must succeed
    """
    reservations = _load_all()
    reservation_exists = any(
        r.reservation_id == reservation.reservation_id
        for r in reservations
    )

    if reservation_exists:
        print(
            "[Reservation] Error: reservation_id already exists: "
            f"{reservation.reservation_id}"
        )
        return False

    if get_hotel(reservation.hotel_id) is None:
        print(f"[Reservation] Error: hotel not found: {reservation.hotel_id}")
        return False

    if get_customer(reservation.customer_id) is None:
        print(
            "[Reservation] Error: customer not found: "
            f"{reservation.customer_id}"
        )
        return False

    if not reserve_room(reservation.hotel_id):
        # reserve_room prints the reason
        return False

    reservations.append(reservation)
    _save_all(reservations)
    return True


def cancel_reservation(reservation_id: str) -> bool:
    """
    Cancel reservation:
    - must exist
    - increase hotel available rooms (cancel_reservation_room)
    - remove reservation from file
    """
    reservations = _load_all()
    target: Optional[Reservation] = None
    for r in reservations:
        if r.reservation_id == reservation_id:
            target = r
            break

    if target is None:
        print(f"[Reservation] Error: reservation not found: {reservation_id}")
        return False

    if not cancel_reservation_room(target.hotel_id):
        return False

    new_list = [r for r in reservations if r.reservation_id != reservation_id]
    _save_all(new_list)
    return True
