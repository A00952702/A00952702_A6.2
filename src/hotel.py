"""
hotel.py
Hotel entity + persistence operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from src.storage import read_json_list, write_json_list


HOTELS_FILE = "data/hotels.json"


@dataclass
class Hotel:
    """Represents a hotel with rooms available."""
    hotel_id: str
    name: str
    location: str
    total_rooms: int
    available_rooms: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON persistence."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Hotel":
        """Create a Hotel from a dict."""
        return Hotel(
            hotel_id=str(data["hotel_id"]),
            name=str(data["name"]),
            location=str(data["location"]),
            total_rooms=int(data["total_rooms"]),
            available_rooms=int(data["available_rooms"]),
        )


def _load_all() -> list[Hotel]:
    items = read_json_list(HOTELS_FILE)
    return [Hotel.from_dict(x) for x in items]


def _save_all(hotels: list[Hotel]) -> None:
    write_json_list(HOTELS_FILE, [h.to_dict() for h in hotels])


def create_hotel(hotel: Hotel) -> bool:
    """
    Create a hotel. Returns True if created, False if ID already exists.
    """
    hotels = _load_all()
    if any(h.hotel_id == hotel.hotel_id for h in hotels):
        print(f"[Hotel] Error: hotel_id already exists: {hotel.hotel_id}")
        return False

    if hotel.total_rooms < 0 or hotel.available_rooms < 0:
        print("[Hotel] Error: room counts cannot be negative.")
        return False

    if hotel.available_rooms > hotel.total_rooms:
        print("[Hotel] Error: available_rooms cannot exceed total_rooms.")
        return False

    hotels.append(hotel)
    _save_all(hotels)
    return True


def delete_hotel(hotel_id: str) -> bool:
    """
    Delete a hotel by ID. Returns True if deleted, False if not found.
    """
    hotels = _load_all()
    new_list = [h for h in hotels if h.hotel_id != hotel_id]
    if len(new_list) == len(hotels):
        print(f"[Hotel] Error: hotel_id not found: {hotel_id}")
        return False
    _save_all(new_list)
    return True


def get_hotel(hotel_id: str) -> Optional[Hotel]:
    """Get hotel by ID."""
    hotels = _load_all()
    for h in hotels:
        if h.hotel_id == hotel_id:
            return h
    return None


def update_hotel(hotel_id: str, name: str, location: str) -> bool:
    """Update hotel info (name/location)."""
    hotels = _load_all()
    for h in hotels:
        if h.hotel_id == hotel_id:
            h.name = name
            h.location = location
            _save_all(hotels)
            return True

    print(f"[Hotel] Error: hotel_id not found: {hotel_id}")
    return False


def reserve_room(hotel_id: str) -> bool:
    """
    Reserve ONE room (decrease available_rooms by 1).
    Returns True if reserved, False otherwise.
    """
    hotels = _load_all()
    for h in hotels:
        if h.hotel_id == hotel_id:
            if h.available_rooms <= 0:
                print(f"[Hotel] Error: no rooms available in hotel {hotel_id}")
                return False
            h.available_rooms -= 1
            _save_all(hotels)
            return True

    print(f"[Hotel] Error: hotel_id not found: {hotel_id}")
    return False


def cancel_reservation_room(hotel_id: str) -> bool:
    """
    Cancel ONE reservation (increase available_rooms by 1).
    Returns True if ok, False if hotel not found or already full.
    """
    hotels = _load_all()
    for h in hotels:
        if h.hotel_id == hotel_id:
            if h.available_rooms >= h.total_rooms:
                print(
                    "[Hotel] Error: rooms already at max in hotel "
                    f"{hotel_id}"
                )
                return False
            h.available_rooms += 1
            _save_all(hotels)
            return True

    print(f"[Hotel] Error: hotel_id not found: {hotel_id}")
    return False
